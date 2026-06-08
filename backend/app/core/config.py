from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Configuración global de la aplicación SGA-Yau.
    Lee las variables de entorno desde el archivo .env o del sistema.
    """
    PROJECT_NAME: str = "SGA-Yau API"
    DATABASE_URL: str = Field(
        default="postgresql://admin_yau:password123@db:5432/db_yau",
        validation_alias="DATABASE_URL"
    )

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
