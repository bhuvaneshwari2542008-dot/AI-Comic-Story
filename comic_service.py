from uuid import uuid4
from app.config import get_settings
from app.models import Comic, ComicRequest
from app.services.story_generator import StoryGenerationError, StoryGenerator
from app.services.image_generator import ImageGenerator
from app.services.comic_repository import ComicRepository
from app.services.pdf_generator import PDFGenerator

class ComicGenerationError(RuntimeError): pass

class ComicService:
    def __init__(self):
        self.story_generator=StoryGenerator(); self.image_generator=ImageGenerator(); self.repository=ComicRepository(); self.pdf_generator=PDFGenerator()

    async def generate(self, request: ComicRequest) -> Comic:
        try:
            comic_id=uuid4().hex
            story=await self.story_generator.generate(request)
            story=await self.image_generator.generate_all(story,comic_id,request.art_style)
            comic=Comic(comic_id=comic_id,**story.model_dump())
            self.repository.save(comic)
            return comic
        except StoryGenerationError as exc:
            raise ComicGenerationError(str(exc)) from exc
        except Exception as exc:
            raise ComicGenerationError("Comic generation failed. Please try again.") from exc

    def get_comic(self, comic_id: str): return self.repository.get(comic_id)
    def create_pdf(self, comic: Comic):
        path=get_settings().output_directory/comic.comic_id/"comic.pdf"
        return self.pdf_generator.generate(comic,path)
