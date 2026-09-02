# Supported input formats

| Category | Formats in the local application | Processing path |
|---|---|---|
| Plain text / code / structured text | TXT, MD, CSV, JSON, XML, HTML, PY, SQL, RTF | Local parser |
| Documents | PDF, DOCX | Page/paragraph extraction |
| Presentations | PPTX | Slide text extraction |
| Spreadsheets | XLSX | Worksheet rows |
| Images | PNG, JPG/JPEG, WEBP, BMP, GIF | Gemini multimodal description |
| Audio | MP3, WAV, M4A, AAC, OGG | Gemini transcription/summary |
| Video | MP4, MOV, AVI, MPEG/MPG, WEBM, WMV | Gemini visual/audio understanding |

Files that a model/provider cannot process are reported as ingestion errors instead of being silently indexed with missing content.
