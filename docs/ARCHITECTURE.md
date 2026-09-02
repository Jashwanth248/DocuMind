# Architecture

DocuMind separates ingestion from retrieval so new data can be added without rebuilding application code.

```text
User uploads / watched folder
       │
       ▼
File router + validation
       │
       ├── text / CSV / JSON / HTML
       ├── PDF page extraction
       ├── DOCX / PPTX / XLSX extraction
       └── image / audio / video → Gemini multimodal understanding
       │
       ▼
Normalized ContentUnit records
       │
       ▼
semantic chunking → Gemini embeddings → Chroma persistent vector index
       │
       ▼
retrieval → grounded context with source labels → Gemini response
       │
       ├── FastAPI `/ask`
       └── Streamlit conversational UI
```

## Design choices

**One normalized content model.** Every source becomes retrieval-ready text plus source metadata. This keeps retrieval predictable across different media types.

**Persistent local vector store.** Chroma makes the project easy to run on a laptop. The storage boundary is isolated so a managed vector database can replace it later.

**Gemini as a multimodal extraction layer.** Images, audio, and video are converted to grounded retrieval descriptions/transcripts before indexing. The same boundary can later use native multimodal embeddings for selected media.

**Source traceability.** Every chunk carries file name, modality and a page/slide/sheet/chunk locator. Answers receive those labels and must cite them.

**Incremental ingestion.** The upload API, batch folder indexer and optional folder watcher all pass through the same ingestion service.
