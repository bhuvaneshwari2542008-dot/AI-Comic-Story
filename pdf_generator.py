from pathlib import Path
from fpdf import FPDF
from app.models import Comic

class PDFGenerator:
    def generate(self, comic: Comic, output_path: Path) -> Path:
        pdf=FPDF()
        pdf.set_auto_page_break(auto=True,margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica","B",22)
        pdf.multi_cell(0,12,self._latin(comic.title),align="C")
        pdf.set_font("Helvetica",size=11)
        pdf.multi_cell(0,7,self._latin(comic.summary))
        for panel in comic.panels:
            pdf.add_page()
            pdf.set_font("Helvetica","B",15)
            pdf.cell(0,10,f"Panel {panel.panel_number}",new_x="LMARGIN",new_y="NEXT")
            if panel.image_path and Path(panel.image_path).is_file():
                pdf.image(panel.image_path,x=15,w=180,h=135)
            pdf.ln(5)
            pdf.set_font("Helvetica","I",11)
            if panel.narration: pdf.multi_cell(0,7,self._latin(panel.narration))
            pdf.set_font("Helvetica",size=11)
            for line in panel.dialogue:
                pdf.multi_cell(0,7,self._latin(f"{line.speaker}: {line.text}"))
        output_path.parent.mkdir(parents=True,exist_ok=True)
        pdf.output(str(output_path))
        return output_path

    @staticmethod
    def _latin(text: str) -> str:
        return text.encode("latin-1","replace").decode("latin-1")
