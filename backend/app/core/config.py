import os


class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "CoCoCreator Admin API")
    API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
    ENV = os.getenv("ENV", "local")
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/cococreator_admin",
    )


settings = Settings()
