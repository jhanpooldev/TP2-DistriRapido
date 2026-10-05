import time
import threading
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.v1.endpoints.dependencies import get_current_operador
from app.core.config import get_settings

router = APIRouter()

settings = get_settings()

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "EcoLogisticaLima/1.0 (proyecto academico TP2)"

MIN_INTERVAL = 1.1
TIMEOUT = 15.0
CACHE_TTL = 600

_cache: dict = {}
_cache_lock = threading.Lock()
_throttle_lock = threading.Lock()
_last_call = 0.0


def _cache_get(key):
    with _cache_lock:
        entry = _cache.get(key)
        if not entry:
            return None
        expires, value = entry
        if expires < time.time():
            _cache.pop(key, None)
            return None
        return value


def _cache_set(key, value):
    with _cache_lock:
        if len(_cache) > 300:
            for k in [k for k, (_, exp) in _cache.items() if exp < time.time()]:
                _cache.pop(k, None)
        _cache[key] = (time.time() + CACHE_TTL, value)


def _consultar(url: str, params: dict) -> httpx.Response:
    global _last_call

    ultimo_error = None

    for intento in range(2):
        with _throttle_lock:
            espera = MIN_INTERVAL - (time.time() - _last_call)
            if espera > 0:
                time.sleep(espera)
            _last_call = time.time()

        try:
            response = httpx.get(
                url,
                params=params,
                headers={"User-Agent": USER_AGENT, "Accept-Language": "es"},
                timeout=TIMEOUT,
            )
        except httpx.HTTPError as exc:
            ultimo_error = f"El servicio de mapas no respondio ({type(exc).__name__})."
            time.sleep(1.0)
            continue

        if response.status_code in (403, 429, 502, 503, 504):
            ultimo_error = (
                "El servicio de busqueda esta saturado temporalmente. "
                "Puedes marcar la ubicacion haciendo click en el mapa."
            )
            time.sleep(1.5 * (intento + 1))
            continue

        return response

    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=ultimo_error or "Servicio de mapas no disponible",
    )


def _compose_direccion(data: dict, latitud: float, longitud: float) -> str:
    direccion = data.get("address", {})
    nombre = data.get("name") or ""

    contexto = [
        direccion.get("city") or direccion.get("town") or direccion.get("county"),
        direccion.get("state"),
    ]
    contexto = [c for c in dict.fromkeys([c for c in contexto if c])]

    if nombre:
        return ", ".join([nombre] + contexto[:1]) if contexto else nombre

    partes = [
        direccion.get("road"),
        direccion.get("neighbourhood"),
        direccion.get("suburb"),
        direccion.get("city_district") or direccion.get("district"),
    ]
    partes = [p for p in dict.fromkeys([p for p in partes if p])]

    if not partes:
        partes = [data.get("display_name", "").split(",")[0]]

    texto = ", ".join(partes[:3])
    if not texto:
        texto = data.get("display_name", f"{latitud:.6f}, {longitud:.6f}")

    return texto


@router.get("/search")
def search_direcciones(
    q: str = Query(..., min_length=2, max_length=120),
    operador=Depends(get_current_operador),
):
    clave = ("search", q.strip().lower())

    en_cache = _cache_get(clave)
    if en_cache is not None:
        return en_cache

    response = _consultar(
        NOMINATIM_SEARCH_URL,
        {
            "q": q.strip(),
            "format": "jsonv2",
            "limit": 8,
            "addressdetails": 1,
            "countrycodes": "pe",
            "viewbox": (
                f"{settings.HOME_LNG - 0.4},{settings.HOME_LAT + 0.25},"
                f"{settings.HOME_LNG + 0.4},{settings.HOME_LAT - 0.25}"
            ),
        },
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El servicio de busqueda no esta disponible en este momento",
        )

    resultados = []
    for item in response.json():
        try:
            lat = float(item["lat"])
            lon = float(item["lon"])
        except (KeyError, TypeError, ValueError):
            continue

        resultados.append({
            "latitud": lat,
            "longitud": lon,
            "direccion": _compose_direccion(item, lat, lon),
            "descripcion": item.get("display_name", ""),
            "tipo": item.get("type") or item.get("class") or "",
        })

    payload = {"resultados": resultados}
    _cache_set(clave, payload)
    return payload


@router.get("/reverse")
def reverse_geocode(
    latitud: float = Query(..., ge=-90, le=90),
    longitud: float = Query(..., ge=-180, le=180),
    operador=Depends(get_current_operador),
):
    clave = ("reverse", round(latitud, 6), round(longitud, 6))

    en_cache = _cache_get(clave)
    if en_cache is not None:
        return en_cache

    response = _consultar(
        NOMINATIM_URL,
        {
            "format": "jsonv2",
            "lat": latitud,
            "lon": longitud,
            "zoom": 18,
            "addressdetails": 1,
        },
    )

    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro una direccion para esas coordenadas",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El servicio de direcciones no esta disponible en este momento",
        )

    data = response.json()

    payload = {
        "latitud": latitud,
        "longitud": longitud,
        "direccion": _compose_direccion(data, latitud, longitud),
        "direccion_completa": data.get("display_name", ""),
    }
    _cache_set(clave, payload)
    return payload