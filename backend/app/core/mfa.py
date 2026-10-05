import base64
import hashlib
import io
import secrets
import string
from typing import List, Tuple
import pyotp
import qrcode

from backend.app.core.config import settings

def generate_totp_secret() -> str:
    """
    Genera una clave secreta aleatoria Base32 de 160 bits (RFC 6238).
    """
    return pyotp.random_base32()

def get_totp_uri(secret: str, email: str) -> str:
    """
    Genera el URI estándar otpauth:// compatible con Google Authenticator.
    """
    totp = pyotp.TOTP(secret, interval=settings.TOTP_INTERVAL_SECONDS)
    return totp.provisioning_uri(name=email, issuer_name=settings.TOTP_ISSUER_NAME)

def generate_qr_code_data_url(otpauth_uri: str) -> str:
    """
    Genera una imagen QR en memoria y la retorna codificada como un Data URL en Base64.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=3,
    )
    qr.add_data(otpauth_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_img}"

def verify_totp_code(secret: str, code: str) -> bool:
    """
    Verifica un código de 6 dígitos dentro de la ventana de tiempo configurada (±30s).
    """
    if not secret or not code:
        return False
    # Asegura que sean 6 dígitos
    code_clean = str(code).strip()
    if len(code_clean) != 6 or not code_clean.isdigit():
        return False
        
    totp = pyotp.TOTP(secret, interval=settings.TOTP_INTERVAL_SECONDS)
    return totp.verify(code_clean, valid_window=settings.TOTP_WINDOW_SKEW)

def hash_recovery_code(code: str) -> str:
    """
    Genera el hash SHA-256 de un código de respaldo para almacenamiento seguro.
    """
    return hashlib.sha256(code.strip().upper().encode("utf-8")).hexdigest()

def generate_backup_recovery_codes(count: int = 5) -> Tuple[List[str], List[str]]:
    """
    Genera una lista de códigos de respaldo alfanuméricos legibles de 8 caracteres.
    Retorna: (codigos_en_claro, codigos_hasheados)
    """
    charset = string.ascii_uppercase + string.digits
    # Excluye caracteres ambiguos como '0', 'O', 'I', '1'
    unambiguous_chars = [c for c in charset if c not in ("0", "O", "I", "1")]
    
    plain_codes = []
    hashed_codes = []
    for _ in range(count):
        # Código de formato: XXXX-XXXX
        part1 = "".join(secrets.choice(unambiguous_chars) for _ in range(4))
        part2 = "".join(secrets.choice(unambiguous_chars) for _ in range(4))
        code = f"{part1}-{part2}"
        plain_codes.append(code)
        hashed_codes.append(hash_recovery_code(code))
        
    return plain_codes, hashed_codes
