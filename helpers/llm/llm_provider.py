from abc import ABC, abstractmethod
from typing import Dict

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def extract_information(self, text: str, query: str) -> Dict:
        """Extract relevant information from the given text using LLM."""
        pass
