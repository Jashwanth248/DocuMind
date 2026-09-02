from __future__ import annotations
import hashlib
import shutil
from pathlib import Path
from .chunking import chunk_text
from .config import settings
from .gemini import GeminiGateway
from .loaders.pdf import load_pdf
from .loaders.text import load_textual
from .loaders.media import load_media
from .schemas import ContentUnit


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def copy_into_library(path: Path) -> Path:
    target = settings.upload_dir / path.name
    if path.resolve() != target.resolve():
        shutil.copy2(path, target)
    return target


def extract_units(path: Path, gateway: GeminiGateway | None = None) -> list[ContentUnit]:
    source_id = file_sha256(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        units = load_pdf(path, source_id)
        if units:
            return units
    units = load_textual(path, source_id)
    if units:
        return units
    gateway = gateway or GeminiGateway()
    return load_media(path, source_id, gateway)


def chunk_units(units: list[ContentUnit]) -> list[ContentUnit]:
    out = []
    for unit in units:
        chunks = chunk_text(unit.text)
        for i, chunk in enumerate(chunks):
            locator = unit.locator
            if len(chunks) > 1:
                locator = f"{locator + ', ' if locator else ''}chunk {i+1}"
            out.append(ContentUnit(unit.source_id, unit.source_name, unit.source_path, unit.modality, chunk, locator, unit.metadata))
    return out
