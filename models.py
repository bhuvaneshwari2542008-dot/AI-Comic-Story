from pydantic import BaseModel, Field, field_validator

class ComicRequest(BaseModel):
    story_prompt: str = Field(min_length=10, max_length=1000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(min_length=1, max_length=150)
    story_tone: str = Field(min_length=1, max_length=50)
    art_style: str = Field(min_length=1, max_length=100)
    panel_count: int = Field(default=5, ge=1, le=6)

    @field_validator("story_prompt", "character_name", "setting", "story_tone", "art_style")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

class Dialogue(BaseModel):
    speaker: str
    text: str

class ComicPanel(BaseModel):
    panel_number: int
    scene: str
    narration: str = ""
    dialogue: list[Dialogue] = Field(default_factory=list)
    image_prompt: str
    image_url: str | None = None
    image_path: str | None = None

class ComicStory(BaseModel):
    title: str
    summary: str
    character_description: str
    panels: list[ComicPanel]

class Comic(ComicStory):
    comic_id: str
