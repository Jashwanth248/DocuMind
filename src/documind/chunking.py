def chunk_text(text: str, chunk_size: int = 1400, overlap: int = 180) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end]
        if end < len(text):
            boundary = max(chunk.rfind(". "), chunk.rfind("\n"))
            if boundary > chunk_size * 0.6:
                end = start + boundary + 1
                chunk = text[start:end]
        chunks.append(chunk.strip())
        if end == len(text):
            break
        start = max(start + 1, end - overlap)
    return [c for c in chunks if c]
