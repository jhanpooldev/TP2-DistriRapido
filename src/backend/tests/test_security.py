"""Pruebas de seguridad. Cubre EN-02."""
import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import get_settings
from app.core.security import create_access_token, decode_token, hash_password, verify_password

settings = get_settings()


def test_hash_y_verificacion_de_password():
    hash1 = hash_password("secreto123")
    hash2 = hash_password("secreto123")

    assert hash1 != "secreto123"
    assert hash1 != hash2
    assert verify_password("secreto123", hash1) is True
    assert verify_password("otra-cosa", hash1) is False


def test_token_valido_se_decodifica():
    token = create_access_token({"sub": str(uuid.uuid4())})
    payload = decode_token(token)

    assert payload is not None
    assert "sub" in payload
    assert "exp" in payload


def test_token_invalido_devuelve_none():
    assert decode_token("no-es-un-token") is None


def test_token_firmado_con_otra_clave_se_rechaza():
    forjado = jwt.encode(
        {"sub": str(uuid.uuid4()), "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        "clave-del-atacante",
        algorithm="HS256",
    )
    assert decode_token(forjado) is None


def test_token_expirado_se_rechaza():
    """EN-02: un token expirado no debe permitir el acceso."""
    expirado = jwt.encode(
        {"sub": str(uuid.uuid4()), "exp": datetime.now(timezone.utc) - timedelta(hours=1)},
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    assert decode_token(expirado) is None


def test_create_access_token_siempre_asigna_caducidad():
    """La expiracion impuesta por el servidor prevalece sobre la del llamador."""
    token = create_access_token({"sub": str(uuid.uuid4()), "exp": datetime.now(timezone.utc) - timedelta(days=1)})
    payload = decode_token(token)

    assert payload is not None
    assert payload["exp"] > datetime.now(timezone.utc).timestamp()