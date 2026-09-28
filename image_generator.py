import asyncio
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from app.config import get_settings
from app.models import ComicStory

class ImageGenerator:
    async def generate_all(self, story: ComicStory, comic_id: str, art_style: str) -> ComicStory:
        for panel in story.panels:
            path = await asyncio.to_thread(self._create_placeholder, comic_id, panel.panel_number, panel.scene, art_style)
            panel.image_path = str(path)
            panel.image_url = "/static/generated/" + str(path.relative_to(get_settings().output_directory)).replace("\\", "/")
        return story

    def _create_placeholder(self, comic_id: str, number: int, scene: str, art_style: str) -> Path:
        directory = get_settings().output_directory / comic_id
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"panel_{number}.png"
        colors=[("#6D3DF5","#FFCA3A"),("#0B7285","#99E9F2"),("#C2255C","#FCC2D7"),("#2B8A3E","#B2F2BB"),("#E8590C","#FFE8CC"),("#364FC7","#D0EBFF")]
        bg,accent=colors[(number-1)%len(colors)]
        image=Image.new("RGB",(960,720),bg)
        draw=ImageDraw.Draw(image)
        draw.rounded_rectangle((60,55,900,665),radius=36,fill=accent,outline="#17151d",width=12)
        draw.ellipse((350,150,610,410),fill="#ffffff",outline="#17151d",width=10)
        draw.ellipse((420,230,455,270),fill="#17151d")
        draw.ellipse((505,230,540,270),fill="#17151d")
        draw.arc((425,255,540,340),start=15,end=165,fill="#17151d",width=8)
        font=ImageFont.load_default()
        text=f"PANEL {number}\n{art_style}\n{scene[:95]}"
        draw.multiline_text((100,485),text,fill="#17151d",font=font,spacing=12)
        image.save(path,"PNG")
        return path
