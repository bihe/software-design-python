import threading
from typing import Any

from .cache import Cache

# we need to ensure that we do not have race-conditions during access
mutex = threading.Lock()


class MemoryCache(Cache):
    """the MemoryCache is a very, very simple implemantation which stores value in a backing-dictionary"""

    def __init__(self):
        self._cache_store = {}

    def put(self, key: str, value: Any):
        with mutex:
            self._cache_store[key] = value

    def get(self, key: str) -> Any:
        with mutex:
            if key in self._cache_store:
                return self._cache_store[key]
            return None

    def delete(self, key: str):
        with mutex:
            if key in self._cache_store:
                del self._cache_store[key]
