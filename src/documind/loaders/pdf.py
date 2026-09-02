from pathlib import Path
import fitz
from ..schemas import ContentUnit


def load_pdf(path: Path, source_id: str) -> list[ContentUnit]:
    doc = fitz.open(path)
    units = []
    for page_no, page in enumerate(doc, 1):
        text = page.get_text("text").strip()
        if text:
            units.append(ContentUnit(source_id, path.name, str(path), "pdf", text, f"page {page_no}"))
    return units
