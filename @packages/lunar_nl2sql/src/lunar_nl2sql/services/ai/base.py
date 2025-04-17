from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AIService(ABC):
    _client = None

    def __init__(self):
        pass

    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to the AI service. Must be implemented by subclasses."""
        pass

    @property
    def client(self):
        """Get the API client, connecting if necessary."""
        if self._client is None:
            self.connect()
        return self._client

    @abstractmethod
    def run(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Run a request to the AI service. Must be implemented by subclasses."""
        pass
