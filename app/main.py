from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.routes import router

APP_DIR = Path(__file__).resolve().parent
settings = get_settings()
app = FastAPI(title=settings.app_name, description="AI-powered comic story creator", version="1.0.0")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
app.mount("/generated", StaticFiles(directory=settings.output_directory), name="generated")
app.include_router(router)
