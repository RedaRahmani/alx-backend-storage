#!/usr/bin/env python3
"""Stores input in the redis client. """


import redis
import uuid
from functools import wraps
from typing import Union, Callable


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function. """
    client = redis.Redis()
    inputs = client.lrange("{}:inputs".format(method.__qualname__), 0, -1)
    outputs = client.lrange("{}:outputs".format(method.__qualname__), 0, -1)

    no_of_calls = len(inputs)
    print(f'{method.__qualname__} was called {no_of_calls} times:')
    for call in zip(inputs, outputs):
        input, output = call[0].decode(), call[1].decode()
        print(f'{method.__qualname__}(*{input}) -> {output}')


def count_calls(method: Callable) -> Callable:
    """Counts how many times methods of the Cache class are called. """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function. """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        k_input = method.__qualname__ + ':inputs'
        self._redis.rpush(k_input, str(args))

        output = method(self, *args, **kwds)
        k_output = method.__qualname__ + ':outputs'
        self._redis.rpush(k_output, output)

        return output
    return wrapper


class Cache:
    """Caches data.

    Attributes:
        _redis: store an instance of the Redis client
    """

    def __init__(self):
        """Initializes a cache instance. """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes a data argument and stores it in redis using
        a random key. """
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """Retrieves and converts the data back to the desired format. """
        if key is None:
            return None

        data = self._redis.get(key)
        return fn(data) if fn else data if data else None

    def get_str(self, key: str) -> str:
        """Retrieves and converts the data to string. """
        try:
            return str(self._redis.get(key))
        except Exception:
            return None

    def get_int(self, key: str) -> int:
        """Retrieves and converts the data to int. """
        try:
            return int(self._redis.get(key))
        except Exception:
            return None
