__all__ = (
    'settings',
)

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB settings
    DATABASE_URL: str

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60

    # PORTS
    APP_PORT: int = 8015
    HR_CORE_GRPC_HOST: str = 500051

    class Config:
        env_file = ".env"

settings = Settings()

