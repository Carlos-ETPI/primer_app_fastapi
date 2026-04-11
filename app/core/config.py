from typing import Annotated, Any, Optional
from environs import env
from pydantic import AnyUrl, BeforeValidator,computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):

    """Configuración de la aplicación, cargada desde variables de entorno o un archivo .env"""
    PROJECT_NAME: str = "Modulo Inventarios"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    """Configuración de la base de datos"""
    DATABASE_URL : str

    """Configuración de seguridad y autenticación"""
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:3000"

    """configuracion del model configura el archivo .env y la codificacion del mismo, ademas de ignorar variables extra"""
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    """Ejemplo de API Key para clientes externos (no usuarios humanos)"""
    API_KEY : str


    BACKEND_CORS_ORIGINS: Annotated[
            list[AnyUrl] | str, BeforeValidator(parse_cors)
        ] = []
    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

settings = Settings()

print(settings.DATABASE_URL)