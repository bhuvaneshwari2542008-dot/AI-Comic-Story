import logging
from pathlib import Path
from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from app.models import ComicRequest
from app.services.comic_service import ComicGenerationError, ComicService

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
comic_service = ComicService()

@router.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"form_data": {}, "error": None})

@router.post("/generate", response_class=HTMLResponse, name="generate_comic")
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    story_tone: str = Form(...),
    art_style: str = Form(...),
    panel_count: int = Form(5),
):
    data = locals().copy(); data.pop("request")
    try:
        comic_request = ComicRequest(**data)
        comic = await comic_service.generate(comic_request)
        return templates.TemplateResponse(request=request, name="comic_preview.html", context={"comic": comic})
    except ValidationError as exc:
        return templates.TemplateResponse(request=request, name="index.html", context={"form_data": data, "error": "Please check the entered information.", "validation_errors": exc.errors()}, status_code=422)
    except ComicGenerationError as exc:
        logger.warning("Comic generation failed: %s", exc)
        return templates.TemplateResponse(request=request, name="error.html", context={"message": str(exc), "retry_url": request.url_for("home")}, status_code=503)
    except Exception:
        logger.exception("Unexpected generation error")
        return templates.TemplateResponse(request=request, name="error.html", context={"message": "An unexpected error occurred. Please try again.", "retry_url": request.url_for("home")}, status_code=500)

@router.post("/api/comics", status_code=status.HTTP_201_CREATED, name="create_comic_api")
async def create_comic_api(comic_request: ComicRequest):
    try:
        return await comic_service.generate(comic_request)
    except ComicGenerationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

@router.get("/comic/{comic_id}", response_class=HTMLResponse, name="comic_preview")
async def comic_preview(request: Request, comic_id: str):
    comic = comic_service.get_comic(comic_id)
    if comic is None:
        return templates.TemplateResponse(request=request, name="error.html", context={"message": "The requested comic could not be found.", "retry_url": request.url_for("home")}, status_code=404)
    return templates.TemplateResponse(request=request, name="comic_preview.html", context={"comic": comic})

@router.get("/comic/{comic_id}/pdf", name="download_comic_pdf")
async def download_comic_pdf(comic_id: str):
    comic = comic_service.get_comic(comic_id)
    if comic is None:
        raise HTTPException(status_code=404, detail="Comic not found.")
    try:
        pdf_path = comic_service.create_pdf(comic)
    except Exception as exc:
        logger.exception("PDF generation failed")
        raise HTTPException(status_code=500, detail="The comic PDF could not be generated.") from exc
    path = Path(pdf_path)
    return FileResponse(path=path, media_type="application/pdf", filename=f"comiccraft-{comic_id}.pdf")

@router.get("/health", name="health_check")
async def health_check():
    return {"status": "ok", "application": "ComicCraft"}
