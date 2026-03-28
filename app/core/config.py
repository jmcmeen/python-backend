from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Python Backend"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./app.db"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30

    model_config = {"env_file": ".env"}


settings = Settings()
