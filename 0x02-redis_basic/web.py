#!/usr/bin/env python3
"""An expiring web cache and tracker"""
import redis
import requests
from typing import Callable

redis = redis.Redis()


def get_page(url: str) -> str:
    """Uses requests to get the content of a webpage."""
    key = f"count:{url}"
    redis.incr(key)
    redis.expire(key, 10)
    return requests.get(url).text
