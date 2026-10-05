from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "distrirapido"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_NAME_TEST: str = "distrirapido_test"

    JWT_SECRET: str = "clave-secreta-super-segura-para-desarrollo"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 8

    HOME_ADDRESS: str = "Av. Javier Prado Este 4200, Surco, Lima"
    HOME_LAT: float = -12.115
    HOME_LNG: float = -76.97

    MAP_PROVIDER: str = "haversine"
    MAX_PUNTOS_POR_RUTA: int = 20

    class Config:
        env_file = "../../.env"
        case_sensitive = True
        extra = "allow"

@lru_cache
def get_settings() -> Settings:
    return Settings()