import time


def measure_the_running_time(f):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = f(*args, **kwargs)
        running_time = time.perf_counter() - start_time
        return result, running_time

    return wrapper
