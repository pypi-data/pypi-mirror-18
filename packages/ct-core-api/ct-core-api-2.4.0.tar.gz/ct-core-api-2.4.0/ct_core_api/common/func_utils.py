from datetime import datetime, timedelta

import inspect
import functools


def memoize(timeout=None):
    def memoize_decorator(fn):
        cache = fn.cache = {}

        @functools.wraps(fn)
        def memoizer(*args, **kwargs):
            kwargs.update(dict(zip(inspect.getargspec(fn).args, args)))
            key = tuple(kwargs.get(k, None) for k in inspect.getargspec(fn).args)

            if key in cache:
                result, timestamp = cache[key]

                if timestamp is not None and timestamp < datetime.now():
                    cache[key] = (fn(**kwargs), datetime.now() + timedelta(seconds=timeout))

            elif timeout is not None:
                cache[key] = (fn(**kwargs), datetime.now() + timedelta(seconds=timeout))
            else:
                cache[key] = (fn(**kwargs), None)

            return cache[key][0]
        return memoizer
    return memoize_decorator
