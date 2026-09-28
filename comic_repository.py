import json
from pathlib import Path
from app.config import get_settings
from app.models import Comic

class ComicRepository:
    def save(self, comic: Comic) -> None:
        directory=get_settings().output_directory/comic.comic_id
        directory.mkdir(parents=True,exist_ok=True)
        (directory/"comic.json").write_text(comic.model_dump_json(indent=2),encoding="utf-8")

    def get(self, comic_id: str) -> Comic | None:
        if not comic_id.replace("-","").isalnum():
            return None
        path=get_settings().output_directory/comic_id/"comic.json"
        if not path.is_file(): return None
        return Comic.model_validate_json(path.read_text(encoding="utf-8"))
