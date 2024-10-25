#!/usr/bin/env python3
"""Cache class module for simple cache implementation using redis"""
import redis
from uuid import uuid4


class Cache:
    """Simple cache implementation using redis"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: any) -> str:
        """Stores data in a random generated key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key
