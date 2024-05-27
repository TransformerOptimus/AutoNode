import functools
import time


class RetryLimitExceededError(Exception):
    """Exception raised when retry attempts are exhausted."""
    def __init__(self):
        super().__init__("Maximum retry limit exceeded")


def retry(max_attempts=3, backoff=1, exceptions=(Exception,)):
    """
    A decorator for retrying a function up to `max_attempts` times,
    with a delay of `delay_seconds` between attempts.

    Args:
    - max_attempts (int): The maximum number of attempts.
    - delay_seconds (int or float): The number of seconds to wait between attempts.
    """
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise RetryLimitExceededError
                    print(f"Attempt {attempts}/{max_attempts} failed : {e}. Retrying in {backoff ** attempts} seconds...")
                    time.sleep(backoff ** attempts)
        return wrapper_retry
    return decorator_retry
