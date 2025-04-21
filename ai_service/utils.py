from time import time


def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"\nFunction {func.__name__!r} executed in {(t2-t1):.4f}s\n")
        return result

    return wrap_func
