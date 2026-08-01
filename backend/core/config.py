from functools import lru_cache
from typing import Literal
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    environment: Literal["development", "test", "staging", "production"] = "development"
    debug: bool = False
    database_url: str = "postgresql+psycopg://chronos:chronos@localhost:5432/chronos"
    secret_key: str = Field(min_length=16, default="change-this-development-secret")
    cors_origins: str = "http://localhost:5173"
    github_client_id: str = ""
    github_client_secret: str = ""
    github_callback_url: str = ""
    enable_demo_auth: bool = True
    log_level: str = "INFO"
    @property
    def allowed_origins(self) -> list[str]: return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

@lru_cache
def get_settings() -> Settings: return Settings()
