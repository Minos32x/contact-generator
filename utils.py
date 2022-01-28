from functools import wraps
import datetime


def execution_time_calculator(func):
    def inner(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print("Total Time -> ", end_time - start_time)

        return result

    return inner
