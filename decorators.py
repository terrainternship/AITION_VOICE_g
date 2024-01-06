import time
import functools
from typing import Callable, Any, Dict

PLUGINS: Dict[str, Callable] = dict()


def register(func: Callable) -> Callable:
    PLUGINS[func.__name__] = func
    return func


def timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        started_at = time.time()
        result = func(*args, **kwargs)
        finished_at = time.time()
        duration = round(finished_at - started_at, 4)
        print(f'Duration: {duration}')

        return result

    return wrapper


def logging(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        result = func(*args, **kwargs)
        print(f'function: {func.__name__}\n args: {args}\n kwargs: {kwargs}')

        return result

    return wrapper


def counter(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        wrapper.count += 1
        result = func(*args, **kwargs)
        print(f'Function: {func.__name__} was called {wrapper.count} times')

        return result

    wrapper.count = 0
    return wrapper
