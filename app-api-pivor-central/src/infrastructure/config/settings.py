from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_key: str = "dev-secret-change-me"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
