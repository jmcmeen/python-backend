from typing import Literal

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Python Backend"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://app:app@localhost:5432/app"
    secret_key: SecretStr
    access_token_expire_minutes: int = 30
    cors_origins: list[str] = []
    log_level: str = "INFO"
    log_format: Literal["json", "console"] = "json"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("secret_key")
    @classmethod
    def _reject_placeholder_secret(cls, v: SecretStr) -> SecretStr:
        marker = v.get_secret_value().lower()
        if "replace-with" in marker or "change-me" in marker:
            raise ValueError(
                "SECRET_KEY contains a placeholder value; generate one with `openssl rand -hex 32`"
            )
        return v


settings = Settings()  # type: ignore[call-arg]  # pydantic-settings reads required fields from env
