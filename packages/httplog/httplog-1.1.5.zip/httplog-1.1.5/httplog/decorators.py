from functools import wraps


def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            if func.__name__ == 'process_response':
                return args[2]
    return wrapper
