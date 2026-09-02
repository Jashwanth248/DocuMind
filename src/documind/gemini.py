from __future__ import annotations
import time
from pathlib import Path
from google import genai
from .config import settings


class GeminiGateway:
    def __init__(self):
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is missing. Copy .env.example to .env and add your key.")
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def describe_media(self, path: Path) -> str:
        uploaded = self.client.files.upload(file=path)
        for _ in range(120):
            current = self.client.files.get(name=uploaded.name)
            state = getattr(getattr(current, "state", None), "name", None)
            if state in (None, "ACTIVE"):
                uploaded = current
                break
            if state == "FAILED":
                raise RuntimeError(f"Gemini failed to process {path.name}")
            time.sleep(2)
        prompt = (
            "Create retrieval-ready metadata for this file. Preserve factual details. "
            "For images describe visible text, objects, tables, diagrams and relationships. "
            "For audio produce a concise transcript/summary with speakers or topics when possible. "
            "For video summarize scenes, spoken content, visible text, products, events and timestamps when possible. "
            "Do not invent details that are not present."
        )
        response = self.client.models.generate_content(
            model=settings.documind_chat_model, contents=[uploaded, prompt]
        )
        return response.text or ""

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = []
        for text in texts:
            result = self.client.models.embed_content(
                model=settings.documind_embed_model, contents=text
            )
            vectors.append(result.embeddings[0].values)
        return vectors

    def answer(self, question: str, context: str) -> str:
        system = (
            "You are DocuMind, a private knowledge assistant. Answer using only the supplied context. "
            "If the context is insufficient, say that the indexed sources do not contain enough information. "
            "Cite sources inline using the provided [Source: ...] labels. Do not fabricate citations."
        )
        prompt = f"{system}\n\nCONTEXT:\n{context}\n\nQUESTION:\n{question}"
        response = self.client.models.generate_content(model=settings.documind_chat_model, contents=prompt)
        return response.text or ""
