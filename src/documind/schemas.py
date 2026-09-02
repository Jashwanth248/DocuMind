from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContentUnit:
    source_id: str
    source_name: str
    source_path: str
    modality: str
    text: str
    locator: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrievedUnit:
    text: str
    source_name: str
    modality: str
    locator: str
    score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
