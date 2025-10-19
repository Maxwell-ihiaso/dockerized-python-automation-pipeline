import time
import random
from typing import Callable, Type, Tuple

def retry(
    exceptions: Tuple[Type[BaseException], ...],
    tries: int = 4,
    base_delay: float = 0.5,
    jitter: float = 0.3,
):
    """
    A decorator that will retry a function if it raises one of the specified
    exceptions. The delay between retries is doubled each time, and
    jittered by a random amount.

    :param exceptions: A tuple of exception types to catch
    :param tries: The number of times to retry
    :param base_delay: The initial delay between retries
    :param jitter: The amount of random jitter to add to the delay
    """
    
    def decorator(fn: Callable):
        """
        A decorator that wraps a function and retries it if it raises one of
        the specified exceptions. The delay between retries is doubled
        each time, and jittered by a random amount.

        :param fn: The function to wrap
        :return: A function that will retry the wrapped function
        """
        def wrapper(*args, **kwargs):
            """
            A function that wraps the given function and retries it if it raises
            one of the specified exceptions. The delay between retries is
            doubled each time, and jittered by a random amount.

            :param args: The arguments to pass to the wrapped function
            :param kwargs: The keyword arguments to pass to the wrapped function
            :return: The return value of the wrapped function
            """
            attempt = 0
            delay = base_delay
            while True:
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= tries:
                        raise
                    time.sleep(delay + random.uniform(0, jitter))
                    delay *= 2
        return wrapper
    return decorator
