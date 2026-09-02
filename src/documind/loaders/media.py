from pathlib import Path
from ..schemas import ContentUnit
from ..gemini import GeminiGateway

MEDIA_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif",
    ".mp3", ".wav", ".m4a", ".aac", ".ogg",
    ".mp4", ".mov", ".avi", ".mpeg", ".mpg", ".webm", ".wmv",
}


def load_media(path: Path, source_id: str, gateway: GeminiGateway) -> list[ContentUnit]:
    if path.suffix.lower() not in MEDIA_SUFFIXES:
        return []
    description = gateway.describe_media(path)
    modality = "image" if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"} else ("audio" if path.suffix.lower() in {".mp3", ".wav", ".m4a", ".aac", ".ogg"} else "video")
    return [ContentUnit(source_id, path.name, str(path), modality, description)]
