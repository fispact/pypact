import time
from functools import wraps

from pypact.util.exceptions import PypactFrozenException


def freeze_it(cls):
    cls.__frozen = False

    def frozensetattr(self, key, value):
        if self.__frozen and not hasattr(self, key):
            raise PypactFrozenException(
                "Class {} is frozen. Cannot set {} = {}" .format(
                    cls.__name__, key, value))
        else:
            object.__setattr__(self, key, value)

    def init_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.__frozen = True

        return wrapper

    cls.__setattr__ = frozensetattr
    cls.__init__ = init_decorator(cls.__init__)

    return cls


def time_it(method):
    def timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()

        if 'runtime' in kwargs:
            name = kwargs.get('runname', method.__name__.upper())
            kwargs['runtime'][name] = int((te - ts))
            kwargs['runtimeunit'][name] = "seconds"
        else:
            print(
                ' *** Time taken for {0}:  {1:.4g} seconds'.format(method.__name__, (te - ts)))
        return result

    return timed
