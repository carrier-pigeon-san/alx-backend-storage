#!/usr/bin/env python3
"""Cache class module for simple cache implementation using redis"""
import redis
from uuid import uuid4
from typing import Callable, Optional


class Cache:
    """Simple cache implementation using redis"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: any) -> str:
        """Stores data in the cache using a generated key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable[[bytes], any]] = None) -> Optional[any]:
        """Retrieves data from the cache in the desired format"""
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> Optional[str]:
        """Retrieves a string value from the cache."""
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_it(self, key: str) -> Optional[int]:
        """Retrieves an integer value from the cache."""
        return self.get(key, lambda x: int(x))
