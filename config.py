from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    app_env: str = "development"
    gemini_api_key: str = ""
    gemini_text_model: str = "gemini-2.5-flash"
    demo_mode: bool = True
    output_directory: Path = Path("app/static/generated")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.output_directory.mkdir(parents=True, exist_ok=True)
    return settings
