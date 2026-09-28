from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.routes import router

settings = get_settings()
app = FastAPI(title=settings.app_name, description="AI-powered comic story creator", version="1.0.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)
