#!/usr/bin/env python3
"""An expiring web cache and tracker"""
import redis
import requests
from functools import wraps
from typing import Callable

r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Counts how many times get_page has been called."""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function"""
        key = f"count:{url}"
        r.incr(key)
        r.expire(key, 10)
        page = method(url)
        return page
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Uses requests to get the content of a webpage."""
    return requests.get(url).text
