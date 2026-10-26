from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Valores de ejemplo que nunca deben usarse en un ambiente desplegado.
_SECRETOS_INSEGUROS = {
    "clave-secreta-super-segura-para-desarrollo",
    "cambiar_por_una_clave_aleatoria_y_segura",
}


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
    JWT_SECRET: str = "clave-secreta-super-segura-para-desarrollo"
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

    @property
    def origenes_cors(self) -> list[str]:
        """Lista normalizada de origenes permitidos.

        El nombre no repite el del campo CORS_ORIGINS para evitar la ambiguedad
        que SonarQube marca como bloqueante (python:S1845).
        """
        return [origen.strip() for origen in self.CORS_ORIGINS.split(",") if origen.strip()]

    @model_validator(mode="after")
    def validar_secreto_en_ambientes_desplegados(self):
        entorno = self.ENVIRONMENT.strip().lower()
        if entorno in {"staging", "production", "produccion"}:
            if self.JWT_SECRET.strip() in _SECRETOS_INSEGUROS or len(self.JWT_SECRET.strip()) < 32:
                raise ValueError(
                    "JWT_SECRET inseguro: configura una clave aleatoria de al menos "
                    "32 caracteres antes de desplegar en Staging o Produccion."
                )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
