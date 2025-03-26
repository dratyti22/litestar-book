from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
    )

    # Postgres
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "litestar_books"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()
