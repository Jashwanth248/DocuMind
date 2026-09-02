# Security and privacy notes

- `.env`, API keys, service-account files and local indexed content are excluded from Git.
- Uploaded files are stored under `data/uploads/`, which is ignored except for `.gitkeep`.
- The current multimodal pipeline sends image/audio/video content to the configured Gemini API for processing. Do not ingest material you are not permitted to send to that provider.
- The local Chroma index contains extracted text/metadata and should be treated as sensitive if the source collection is sensitive.
- A production deployment should add authentication, per-user/tenant authorization, encrypted object storage, audit logging, malware scanning, retention controls and secret management.
