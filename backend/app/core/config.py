import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "EcoLogistica Lima - Auth & MFA")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Claves criptográficas y tokens
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "ecologistica_super_secret_jwt_key_2026_distrirapido_security_token_change_in_prod"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # Expiración según reglas de negocio (RN-005: 8 horas = 480 min)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
    
    # Token temporal efímero para el paso 2 de MFA
    MFA_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("MFA_TOKEN_EXPIRE_MINUTES", "5"))
    
    # Regla RN-002: Bloqueo por 3 intentos fallidos consecutivos por 15 minutos
    MAX_FAILED_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_FAILED_LOGIN_ATTEMPTS", "3"))
    ACCOUNT_LOCKOUT_MINUTES: int = int(os.getenv("ACCOUNT_LOCKOUT_MINUTES", "15"))
    
    # MFA y TOTP
    TOTP_ISSUER_NAME: str = os.getenv("TOTP_ISSUER_NAME", "EcoLogistica Lima")
    TOTP_INTERVAL_SECONDS: int = 30
    TOTP_WINDOW_SKEW: int = 1  # ±30 segundos de tolerancia

settings = Settings()
