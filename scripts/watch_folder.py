import argparse
import time
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from src.documind.service import DocuMindService

class Handler(FileSystemEventHandler):
    def __init__(self):
        self.service = DocuMindService()
    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        try:
            result = self.service.ingest(path)
            print(f"indexed {path.name}: {result['chunks_indexed']} chunks")
        except Exception as exc:
            print(f"could not index {path.name}: {exc}")

parser = argparse.ArgumentParser()
parser.add_argument("folder", nargs="?", default="data/uploads")
args = parser.parse_args()
path = Path(args.folder); path.mkdir(parents=True, exist_ok=True)
observer = Observer(); observer.schedule(Handler(), str(path), recursive=False); observer.start()
print(f"Watching {path.resolve()} for new files. Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
