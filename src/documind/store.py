from __future__ import annotations
import chromadb
from .config import settings
from .gemini import GeminiGateway
from .schemas import ContentUnit, RetrievedUnit


class KnowledgeStore:
    def __init__(self, gateway: GeminiGateway | None = None):
        self.client = chromadb.PersistentClient(path=str(settings.index_dir))
        self.collection = self.client.get_or_create_collection(name=settings.documind_collection, metadata={"hnsw:space": "cosine"})
        self.gateway = gateway

    def _gateway(self) -> GeminiGateway:
        if self.gateway is None:
            self.gateway = GeminiGateway()
        return self.gateway

    def upsert(self, units: list[ContentUnit]) -> int:
        if not units:
            return 0
        vectors = self._gateway().embed_texts([u.text for u in units])
        ids, docs, metas = [], [], []
        for i, u in enumerate(units):
            ids.append(f"{u.source_id}:{u.locator}:{i}")
            docs.append(u.text)
            metas.append({"source_id": u.source_id, "source_name": u.source_name, "source_path": u.source_path, "modality": u.modality, "locator": u.locator})
        self.collection.upsert(ids=ids, embeddings=vectors, documents=docs, metadatas=metas)
        return len(units)

    def delete_source(self, source_id: str) -> None:
        self.collection.delete(where={"source_id": source_id})

    def search(self, query: str, top_k: int | None = None) -> list[RetrievedUnit]:
        vector = self._gateway().embed_texts([query])[0]
        result = self.collection.query(query_embeddings=[vector], n_results=top_k or settings.documind_top_k)
        rows = []
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        for doc, meta, distance in zip(docs, metas, distances):
            rows.append(RetrievedUnit(doc, meta.get("source_name", ""), meta.get("modality", ""), meta.get("locator", ""), 1-float(distance), meta))
        return rows

    def list_sources(self) -> list[dict]:
        data = self.collection.get(include=["metadatas"])
        seen = {}
        for meta in data.get("metadatas", []):
            if not meta:
                continue
            seen[meta["source_id"]] = {k: meta.get(k, "") for k in ("source_id", "source_name", "modality")}
        return sorted(seen.values(), key=lambda x: x["source_name"].lower())
