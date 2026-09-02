import argparse
from pathlib import Path
from src.documind.service import DocuMindService

parser = argparse.ArgumentParser(description="Index all supported files in a folder")
parser.add_argument("folder", type=Path)
args = parser.parse_args()
svc = DocuMindService()
for path in sorted(args.folder.rglob("*")):
    if not path.is_file() or path.name.startswith("."):
        continue
    try:
        result = svc.ingest(path)
        print(f"indexed {path.name}: {result['chunks_indexed']} chunks")
    except Exception as exc:
        print(f"skipped {path.name}: {exc}")
