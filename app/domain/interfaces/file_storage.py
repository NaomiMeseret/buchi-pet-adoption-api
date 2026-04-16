from abc import ABC, abstractmethod


class FileStorage(ABC):
    @abstractmethod
    def save(self, filename: str, content: bytes) -> str:
        pass
