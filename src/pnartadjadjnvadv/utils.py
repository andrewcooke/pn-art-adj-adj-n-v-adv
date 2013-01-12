
from functools import wraps


def to_list(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        return list(func(*args, **kargs))
    return wrapper

def lmap(f, args):
    return list(map(f, args))

def tmap(f, args):
    return tuple(map(f, args))
