from src.documind.chunking import chunk_text

def test_short_text_stays_single_chunk():
    assert chunk_text("hello world", 100, 10) == ["hello world"]

def test_long_text_chunks_with_overlap():
    text = "Sentence. " * 100
    chunks = chunk_text(text, 120, 20)
    assert len(chunks) > 2
    assert all(chunks)
