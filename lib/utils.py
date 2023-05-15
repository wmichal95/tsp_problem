import time


def timer(function):
    def wrapper(*args, **kwargs):
        time_start = time.perf_counter()
        result = function(*args, **kwargs)
        time_end = time.perf_counter()

        print(f'{function.__name__} took {(time_end - time_start):.3f}s')

        return result

    return wrapper