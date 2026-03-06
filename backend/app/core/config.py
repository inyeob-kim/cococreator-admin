import os


class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "CoCoCreator Admin API")
    API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
    ENV = os.getenv("ENV", "local")
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/cococreator_admin",
    )
    AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "change-me-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "14"))


settings = Settings()
