import secrets
from functools import lru_cache
from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Valores de ejemplo que nunca deben usarse en ningún ambiente.
_SECRETOS_INSEGUROS: set[str] = {
    "clave-secreta-super-segura-para-desarrollo",
    "cambiar_por_una_clave_aleatoria_y_segura",
}


def _secreto_de_desarrollo() -> str:
    """Clave efímera para desarrollo local sin archivo `.env`.

    No se versiona: cada proceso genera la suya. Los tokens emitidos antes de
    reiniciar el servidor dejan de ser válidos, lo que es preferible a firmar
    con una clave conocida por el repositorio.
    """
    return secrets.token_urlsafe(48)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        case_sensitive=True,
        extra="allow",
    )

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "distrirapido"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_NAME_TEST: str = "distrirapido_test"

    ENVIRONMENT: str = "development"
    JWT_SECRET: str = Field(default_factory=_secreto_de_desarrollo)
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 8

    # Origenes permitidos por CORS. En desarrollo se aceptan los dos nombres
    # habituales del frontend de Vite; en Staging/Produccion debe configurarse
    # explicitamente con el dominio real.
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    HOME_ADDRESS: str = "Av. Javier Prado Este 4200, Surco, Lima"
    HOME_LAT: float = -12.115
    HOME_LNG: float = -76.97

    MAP_PROVIDER: str = "haversine"
    MAX_PUNTOS_POR_RUTA: int = 20

    @model_validator(mode="before")
    @classmethod
    def descartar_secreto_de_ejemplo_en_desarrollo(cls, valores: Any) -> Any:
        """Ignora claves conocidas en desarrollo sin impedir el arranque local.

        El repositorio contiene un `.env` local con valores históricos de ejemplo.
        No se modifica ese archivo: en desarrollo la clave se descarta y se
        genera una efímera. En Staging/Producción el valor llega al validador
        posterior y se rechaza.
        """
        if not isinstance(valores, dict):
            return valores
        entorno = str(valores.get("ENVIRONMENT", "development")).strip().lower()
        if entorno in {"staging", "production", "produccion"}:
            return valores
        secreto = str(valores.get("JWT_SECRET", "")).strip()
        if not secreto or secreto in _SECRETOS_INSEGUROS:
            valores = dict(valores)
            valores.pop("JWT_SECRET", None)
        return valores

    @property
    def origenes_cors(self) -> list[str]:
        """Lista normalizada de origenes permitidos.

        El nombre no repite el del campo CORS_ORIGINS para evitar la ambiguedad
        que SonarQube marca como bloqueante (python:S1845).
        """
        return [origen.strip() for origen in self.CORS_ORIGINS.split(",") if origen.strip()]

    @model_validator(mode="after")
    def validar_secreto(self) -> "Settings":
        secreto = self.JWT_SECRET.strip()
        entorno = self.ENVIRONMENT.strip().lower()

        if not secreto or secreto in _SECRETOS_INSEGUROS:
            raise ValueError(
                "JWT_SECRET inseguro: no uses valores de ejemplo ni una clave vacía; "
                "genera una clave aleatoria con `openssl rand -hex 32`."
            )
        if entorno in {"staging", "production", "produccion"}:
            if "JWT_SECRET" not in self.model_fields_set:
                raise ValueError(
                    "JWT_SECRET debe configurarse explícitamente antes de desplegar "
                    "en Staging o Produccion."
                )
            if len(secreto) < 32:
                raise ValueError(
                    "JWT_SECRET inseguro: configura una clave aleatoria de al menos "
                    "32 caracteres antes de desplegar en Staging o Produccion."
                )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
