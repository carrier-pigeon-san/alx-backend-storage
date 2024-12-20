#!/usr/bin/env python3
"""Cache class module for simple cache implementation using redis"""
import redis
from uuid import uuid4
from typing import Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts how many times a method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        self._redis.save()
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of inputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        self._redis.save()
        return output
    return wrapper


class Cache:
    """Simple cache implementation using redis"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in the cache using a generated key"""
        key: str = str(uuid4())
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

    def get_int(self, key: str) -> Optional[int]:
        """Retrieves an integer value from the cache."""
        return self.get(key, lambda x: int(x))


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function"""
    r = redis.Redis()
    method_name = method.__qualname__

    call_count = r.get(method_name)
    call_count = int(call_count.decode('utf-8')) if call_count else 0

    inputs = r.lrange(f"{method_name}:inputs", 0, -1)
    outputs = r.lrange(f"{method_name}:outputs", 0, -1)

    print("{} was called {} times:".format(method_name, call_count))

    for i, (input, output) in enumerate(zip(inputs, outputs), 1):
        print("{}(*{}) -> {}".format(
            method_name,
            input.decode('utf-8'),
            output.decode('utf-8')
            ))
