from pathlib import Path
from uuid import uuid4

from app.domain.interfaces.file_storage import FileStorage


class LocalFileStorage(FileStorage):
    def __init__(self, root_directory: str, base_url: str) -> None:
        self.root_directory = Path(root_directory)
        self.base_url = base_url.rstrip("/")
        self.root_directory.mkdir(parents=True, exist_ok=True)

    def save(self, filename: str, content: bytes) -> str:
        suffix = Path(filename).suffix or ".jpg"
        stored_name = f"{uuid4()}{suffix}"
        destination = self.root_directory / stored_name
        destination.write_bytes(content)
        return f"{self.base_url}/{stored_name}"
