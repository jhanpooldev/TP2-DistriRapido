"""Control de intentos fallidos de inicio de sesión (RN-002).

El estado se mantiene en memoria y por proceso, igual que la revocación de
tokens: no se agrega una tabla ni una dependencia nueva para una política que
el PMV resuelve en el servidor de aplicación. La clave es el correo
normalizado, de modo que intentos con distinta capitalización cuentan como el
mismo usuario y un correo inexistente no pueda usarse para evadir el bloqueo.
"""
from dataclasses import dataclass
from math import ceil
from threading import Lock
from time import monotonic
from typing import Callable, Dict, Optional, Tuple

MAX_INTENTOS_FALLIDOS = 3
MINUTOS_BLOQUEO = 15


@dataclass
class _EstadoIntentos:
    intentos: int = 0
    desbloqueo: float = 0.0


class ControladorIntentosLogin:
    """Acumula fallos consecutivos y bloquea la clave durante 15 minutos."""

    def __init__(
        self,
        max_intentos: int = MAX_INTENTOS_FALLIDOS,
        segundos_bloqueo: int = MINUTOS_BLOQUEO * 60,
        reloj: Callable[[], float] = monotonic,
    ) -> None:
        self.max_intentos = max_intentos
        self.segundos_bloqueo = segundos_bloqueo
        self._reloj = reloj
        self._intentos: Dict[str, _EstadoIntentos] = {}
        self._bloqueo = Lock()

    @staticmethod
    def normalizar_clave(correo: str) -> str:
        return correo.strip().lower()

    def _limpiar_vencidos(self, ahora: float) -> None:
        for clave, estado in list(self._intentos.items()):
            if estado.desbloqueo and estado.desbloqueo <= ahora:
                del self._intentos[clave]

    def consultar(self, correo: str, ahora: Optional[float] = None) -> Tuple[bool, int]:
        """Devuelve (esta_bloqueado, segundos_restantes)."""
        instante = self._reloj() if ahora is None else ahora
        clave = self.normalizar_clave(correo)
        with self._bloqueo:
            self._limpiar_vencidos(instante)
            estado = self._intentos.get(clave)
            if estado is None:
                return False, 0
            restante = max(0, ceil(estado.desbloqueo - instante))
            return estado.intentos >= self.max_intentos, restante

    def registrar_fallo(self, correo: str, ahora: Optional[float] = None) -> Tuple[bool, int]:
        """Registra un fallo y devuelve el estado resultante (RN-002)."""
        instante = self._reloj() if ahora is None else ahora
        clave = self.normalizar_clave(correo)
        with self._bloqueo:
            self._limpiar_vencidos(instante)
            estado = self._intentos.setdefault(clave, _EstadoIntentos())
            estado.intentos += 1
            if estado.intentos >= self.max_intentos:
                estado.desbloqueo = instante + self.segundos_bloqueo
            restante = max(0, ceil(estado.desbloqueo - instante))
            return estado.intentos >= self.max_intentos, restante

    def reiniciar(self, correo: str) -> None:
        """Limpia los fallos consecutivos después de un inicio de sesión correcto."""
        clave = self.normalizar_clave(correo)
        with self._bloqueo:
            self._intentos.pop(clave, None)


# Una sola instancia por proceso, compartida por todas las peticiones.
intentos_login = ControladorIntentosLogin()
