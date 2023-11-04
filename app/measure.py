from time import perf_counter
from functools import wraps
from typing import Any, Callable


def measure_time(print_result_predicate: Callable[[Any], bool]):
    def decorator(fn: Callable[..., Any]):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            tic = perf_counter()
            res: Any = fn(*args, **kwargs)
            toc = perf_counter()
            if print_result_predicate(res):
                print(f"{((toc - tic) * 1000):.0f} ms")
            return res

        return wrapper

    return decorator
