from abc import ABC, abstractmethod
from typing import Dict


class OCRProvider(ABC):
    """Abstract base class for OCR providers."""

    @abstractmethod
    async def extract_text(self, file_path: str) -> str:
        """Extract text from a given PDF file."""
        pass

    @abstractmethod
    async def fetch_text(self, extract_id: str) -> str:
        """Extract text from a given PDF file."""
        pass
