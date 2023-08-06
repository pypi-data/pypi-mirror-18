class ClassProperty(property):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class_property = ClassProperty


def subclasses(cls, _seen=None):
    """Return a generator expression that yields all subclasses of the provided class."""
    if not isinstance(cls, type):
        raise TypeError('subclasses must be called with new-style classes, not %.100r' % cls)

    if _seen is None:
        _seen = set()

    try:
        subs = cls.__subclasses__()
    except TypeError:  # fails only when cls is type
        subs = cls.__subclasses__(cls)

    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub2 in subclasses(sub, _seen):
                yield sub2


class FrozenClass(object):
    """Disable dynamic attribute setting (after :meth:`__init__`).

    Adapted from http://stackoverflow.com/a/3603824/388033
    """
    __isfrozen = False

    def __init__(self):
        self.__isfrozen = True

    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError("%r is a frozen class" % self)
        object.__setattr__(self, key, value)
