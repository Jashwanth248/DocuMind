from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from src.documind.config import settings
from src.documind.service import DocuMindService

app = FastAPI(title="DocuMind API", version="0.1.0")

class AskRequest(BaseModel):
    question: str
    top_k: int | None = None


def service() -> DocuMindService:
    return DocuMindService()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/sources")
def sources():
    return service().store.list_sources()

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    content = await file.read()
    if len(content) > settings.documind_max_upload_mb * 1024 * 1024:
        raise HTTPException(413, "File is larger than the configured upload limit")
    safe_name = Path(file.filename or "upload.bin").name
    path = settings.upload_dir / safe_name
    path.write_bytes(content)
    try:
        return service().ingest(path)
    except Exception as exc:
        raise HTTPException(400, str(exc)) from exc

@app.post("/ask")
def ask(payload: AskRequest):
    if not payload.question.strip():
        raise HTTPException(400, "Question cannot be empty")
    return service().ask(payload.question, payload.top_k)
