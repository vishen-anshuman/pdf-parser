from abc import ABC, abstractmethod
from typing import Dict

from pydantic import BaseModel


class Database(ABC):
    """Abstract base class for database operations."""

    @abstractmethod
    def insert_query(self, table: str, row: BaseModel) -> None:
        """Executes a SQL query."""
        pass

    @abstractmethod
    async def fetch_results(self, table: str, primary_id: str) -> Dict:
        """Fetches results from a SQL query."""
        pass
