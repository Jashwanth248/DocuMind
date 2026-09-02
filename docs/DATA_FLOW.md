# Data flow

1. A user uploads a file in the UI, posts it to `/ingest`, runs `index_folder.py`, or drops it into a watched folder.
2. DocuMind computes a SHA-256 source identifier and stores a local copy.
3. The loader selects the appropriate extractor.
4. Text-bearing files are parsed locally. Images/audio/video are summarized or transcribed by Gemini multimodal understanding.
5. Extracted content is split into overlapping semantic chunks.
6. Chunks are embedded and upserted into the persistent vector collection.
7. A question is embedded and used to retrieve the closest chunks.
8. Retrieved chunks are assembled with explicit `[Source: ...]` labels.
9. Gemini answers only from the retrieved context and returns citations to the UI.

The source identifier is content-based, which provides a foundation for deduplication and future versioning.
