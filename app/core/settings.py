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

    # CORE SERVICE
    HR_CORE_URL: str
    HR_API_SECRET_KEY: str

    # CORS
    ALLOW_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
    ]

    class Config:
        env_file = ".env"


settings = Settings()

