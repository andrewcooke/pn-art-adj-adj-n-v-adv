
from functools import wraps


def to_list(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        return list(func(*args, **kargs))
    return wrapper

def lmap(func, args):
    return list(map(func, args))

def tmap(func, args):
    return tuple(map(func, args))

# http://code.activestate.com/recipes/465057-basic-synchronization-decorator/
def synchronized(lock):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kargs):
            lock.acquire()
            try: return func(*args, **kargs)
            finally: lock.release()
        return wrapper
    return decorator

def latest(container):
    for entry in reversed(container):
        return entry

def latest_dict(dict):
    return dict[latest(dict)]