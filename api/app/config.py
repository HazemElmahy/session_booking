from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration, read from environment variables or a local .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Session Booking API"
    database_url: str = "postgresql+psycopg://booking:booking@localhost:5432/booking"


settings = Settings()
