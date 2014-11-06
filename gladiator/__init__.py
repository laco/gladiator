from .core import validate
from .validators import required, format_email, length_max, length_min, length, type_, lt, gt, eq, ne, gte, lte, _value

__version__ = "0.6"


def get_version():
    return __version__


def next_version():
    _v = __version__.split('.')
    _v[-1] = str(int(_v[-1]) + 1)
    return '.'.join(_v)


__all__ = ['validate',
           'required',
           'format_email',
           'length_max',
           'length_min',
           'length',
           'type_',
           '_value',
           'lt',
           'gt',
           'eq',
           'ne',
           'gte',
           'lte',
           'true_if_empty']
