from datetime import datetime, timedelta, timezone
from threading import Lock
from time import time
from typing import Optional
import uuid
import bcrypt
import jwt
from app.core.config import get_settings

settings = get_settings()

# RF-014: tokens revocados al cerrar sesión. Se guarda el `jti` hasta su
# caducidad natural para que la lista no crezca sin límite.
_revoked_tokens: dict[str, float] = {}
_revoked_lock = Lock()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=settings.JWT_EXPIRE_HOURS))
    # `jti` permite revocar exactamente esta sesión sin afectar a otras.
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def _limpiar_revoked() -> None:
    ahora = time()
    for jti, expiracion in list(_revoked_tokens.items()):
        if expiracion <= ahora:
            del _revoked_tokens[jti]


def revocar_token(token: str) -> bool:
    """Revoca el token actual. Devuelve False si la firma no es válida."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.PyJWTError:
        return False
    jti = payload.get("jti")
    if not jti:
        return False
    with _revoked_lock:
        _limpiar_revoked()
        _revoked_tokens[str(jti)] = float(payload.get("exp", 0))
    return True


def esta_revocado(jti: Optional[str]) -> bool:
    if not jti:
        return False
    with _revoked_lock:
        _limpiar_revoked()
        return str(jti) in _revoked_tokens


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None
    if esta_revocado(payload.get("jti")):
        return None
    return payload
