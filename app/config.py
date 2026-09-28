import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIRECTORY = (
    Path("/tmp") / "comiccraft" / "generated"
    if os.getenv("VERCEL")
    else BASE_DIR / "static" / "generated"
)

class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    app_env: str = "development"
    gemini_api_key: str = ""
    gemini_text_model: str = "gemini-2.5-flash"
    demo_mode: bool = True
    output_directory: Path = DEFAULT_OUTPUT_DIRECTORY
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if os.getenv("VERCEL"):
        settings.output_directory = Path("/tmp") / "comiccraft" / "generated"
    settings.output_directory.mkdir(parents=True, exist_ok=True)
    return settingsimport os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIRECTORY = (
    Path("/tmp") / "comiccraft" / "generated"
    if os.getenv("VERCEL")
    else BASE_DIR / "static" / "generated"
)

class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    app_env: str = "development"
    gemini_api_key: str = ""
    gemini_text_model: str = "gemini-2.5-flash"
    demo_mode: bool = True
    output_directory: Path = DEFAULT_OUTPUT_DIRECTORY
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.output_directory.mkdir(parents=True, exist_ok=True)
    return settings
