from abc import ABC, abstractmethod
from typing import Any


class Cache(ABC):
    """a common cache definition to store and retrieve key/value entries."""

    @abstractmethod
    def put(self, key: str, value: Any):
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def delete(self, key: str):
        pass
