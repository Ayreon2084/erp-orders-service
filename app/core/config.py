"""Application configuration settings."""
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv(override=True)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    # Various:
    app_description: str = "Test task for Python Developer vacancy."
    app_title: str = "ERP Service"
    debug: bool = False

    # POSTGRES:
    db_host: str = "localhost"
    db_name: str
    db_password: str
    db_port: int = 5435
    db_username: str

    @property
    def database_url(self) -> str:
        """Generate PostgreSQL async database URL.

        Returns:
            Database connection URL string.
        """
        return (
            f"postgresql+asyncpg://{self.db_username}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
