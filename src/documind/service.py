from pathlib import Path
from .gemini import GeminiGateway
from .ingest import copy_into_library, extract_units, chunk_units, file_sha256
from .store import KnowledgeStore


class DocuMindService:
    def __init__(self):
        self.gateway = GeminiGateway()
        self.store = KnowledgeStore(self.gateway)

    def ingest(self, path: Path) -> dict:
        stored = copy_into_library(path)
        source_id = file_sha256(stored)
        self.store.delete_source(source_id)
        units = chunk_units(extract_units(stored, self.gateway))
        count = self.store.upsert(units)
        return {"source_id": source_id, "source_name": stored.name, "chunks_indexed": count}

    def ask(self, question: str, top_k: int | None = None) -> dict:
        hits = self.store.search(question, top_k)
        context_parts = []
        citations = []
        for hit in hits:
            label = hit.source_name + (f", {hit.locator}" if hit.locator else "")
            context_parts.append(f"[Source: {label}]\n{hit.text}")
            citations.append({"source": hit.source_name, "locator": hit.locator, "modality": hit.modality, "score": round(hit.score or 0, 4)})
        answer = self.gateway.answer(question, "\n\n".join(context_parts))
        return {"answer": answer, "sources": citations}
