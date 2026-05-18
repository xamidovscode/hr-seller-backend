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
    HR_CORE_GRPC_HOST: str = 'localhost:50051'

    # CORE SERVICE
    HR_CORE_URL: str
    HR_API_SECRET_KEY: str

    # Admin panel
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"

    # CORS
    ALLOW_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
    ]

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # TG BOTS
    SUPPORT_BOT_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()

