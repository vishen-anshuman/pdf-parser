from abc import ABC, abstractmethod
from typing import Dict

class FileStore(ABC):
    """Abstract base class for file storage providers."""

    @abstractmethod
    def upload_file(self, file_path: str, destination: str) -> Dict:
        """Uploads a file and returns its metadata."""
        pass

    @abstractmethod
    def get_file_url(self, file_name: str) -> str:
        """Retrieves a file URL."""
        pass
