import hashlib
import hmac
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import jwt

from backend.app.core.config import settings

def get_password_hash(password: str) -> str:
    """
    Hashea una contraseña utilizando PBKDF2-HMAC-SHA256 con salt criptográfica aleatoria.
    Cumple con RN-004 y lineamientos de OWASP Password Storage.
    Formato retornado: pbkdf2_sha256${iterations}${salt_hex}${hash_hex}
    """
    salt = os.urandom(16)
    iterations = 100_000
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${hash_bytes.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña en texto claro contra el hash almacenado usando tiempo constante.
    """
    try:
        parts = hashed_password.split("$")
        if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
            return False
        iterations = int(parts[1])
        salt = bytes.fromhex(parts[2])
        expected_hash = bytes.fromhex(parts[3])
        calculated_hash = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(calculated_hash, expected_hash)
    except Exception:
        return False

def create_access_token(
    subject: str, 
    role: str,
    email: str,
    expires_delta: Optional[timedelta] = None,
    custom_claims: Optional[Dict[str, Any]] = None
) -> str:
    """
    Genera un Access Token JWT firmado para una sesión activa (8 horas según RN-005).
    Incluye identificador único jti para posibilitar revocación en logout.
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    payload: Dict[str, Any] = {
        "sub": subject,
        "email": email,
        "rol": role,
        "jti": str(uuid.uuid4()),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "scope": "access_token"
    }
    if custom_claims:
        payload.update(custom_claims)
        
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_mfa_token(subject: str, email: str) -> str:
    """
    Genera un token de desafío temporal para el Paso 2 de MFA.
    Expira en 5 minutos y su alcance está restringido estrictamente a la verificación MFA.
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.MFA_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "email": email,
        "jti": str(uuid.uuid4()),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "scope": "mfa_pending"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decodifica y valida la firma y expiración de un token JWT.
    Lanza jwt.PyJWTError si el token es inválido o ha expirado.
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
