"""Compresion Brotli para respuestas HTTP.

Starlette ya incluye GZipMiddleware. Brotli comprime mejor el JSON y los
assets de texto, pero no forma parte de Starlette, por lo que se implementa
aqui con la dependencia opcional `brotli`. Si el paquete no esta instalado o
el cliente no lo acepta, la peticion sigue su curso sin cambios.
"""

try:
    import brotli
except ImportError:  # pragma: no cover - depende del entorno de despliegue
    brotli = None

from starlette.datastructures import Headers, MutableHeaders

_TIPOS_COMPRIMIBLES = (
    "text/",
    "application/json",
    "application/javascript",
    "application/xml",
    "image/svg+xml",
)


class BrotliMiddleware:
    """Comprime respuestas de texto cuando el cliente envia `Accept-Encoding: br`."""

    def __init__(self, app, minimum_size: int = 500, quality: int = 4):
        self.app = app
        self.minimum_size = minimum_size
        self.quality = quality

    async def __call__(self, scope, receive, send):
        if brotli is None or scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        cabeceras = Headers(scope=scope)
        if "br" not in cabeceras.get("accept-encoding", "").lower():
            await self.app(scope, receive, send)
            return

        # Se comprime en esta capa, asi que se pide al resto de la pila que no
        # vuelva a comprimir (evita gzip + brotli sobre el mismo cuerpo).
        scope = dict(scope)
        scope["headers"] = [
            (nombre, valor)
            for nombre, valor in scope["headers"]
            if nombre.lower() != b"accept-encoding"
        ] + [(b"accept-encoding", b"identity")]

        inicio = None
        cuerpo = []

        async def enviar(mensaje):
            nonlocal inicio
            if mensaje["type"] == "http.response.start":
                inicio = mensaje
                return
            if mensaje["type"] == "http.response.body":
                cuerpo.append(mensaje.get("body", b""))
                if mensaje.get("more_body", False):
                    return
                await self._enviar(inicio, b"".join(cuerpo), send)
                return
            await send(mensaje)

        await self.app(scope, receive, enviar)

    async def _enviar(self, inicio, cuerpo: bytes, send):
        if inicio is None:  # respuesta sin cabeceras: no hay nada que comprimir
            return
        cabeceras = MutableHeaders(raw=inicio["headers"])
        tipo = cabeceras.get("content-type", "").lower()
        comprimible = any(tipo.startswith(t) for t in _TIPOS_COMPRIMIBLES)

        if (
            inicio["status"] == 200
            and comprimible
            and len(cuerpo) >= self.minimum_size
            and "content-encoding" not in cabeceras
        ):
            comprimido = brotli.compress(cuerpo, quality=self.quality)
            if len(comprimido) < len(cuerpo):
                cabeceras["content-encoding"] = "br"
                cabeceras["content-length"] = str(len(comprimido))
                cabeceras.add_vary_header("Accept-Encoding")
                cuerpo = comprimido

        await send(inicio)
        await send({"type": "http.response.body", "body": cuerpo, "more_body": False})
