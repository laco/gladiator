from functools import wraps, partial
from .utils import dummy_gettext as _


FALSE_VALUES = (None, '', 0, False)


def true_if_empty(func):
    """If you put this decorator on a validator
    the validator never fail if the value is missing.
    
    If the value is present (not None), the validator will run as expected.
    This is useful, if the key is optional in a dictionary.
    """
    @wraps(func)
    def _validator(obj, selector, ctx):
        if obj is None:
            return True
        else:
            return func(obj, selector, ctx)
    return _validator


def required(obj, selector, ctx):
    return (False, _('missing value.')) if obj in FALSE_VALUES else True


@true_if_empty
def format_email(obj, selector, ctx):
    return (False, _('bad email format')) if '@' not in obj else True


def length(minimum, maximum):
    _msg_ctx = {
        'minimum': minimum,
        'maximum': maximum
    }

    @true_if_empty
    @wraps(length)
    def _validator(obj, selector, ctx):
        if minimum is not None and maximum is not None:
            if not (len(obj) >= minimum and len(obj) <= maximum):
                return False, _('Must be between {minimum} and {maximum}'), _msg_ctx
        elif minimum is None and maximum is not None:
            if not len(obj) <= maximum:
                return False, _('Must be less then {maximum}'), _msg_ctx
        elif minimum is not None and maximum is None:
            if not len(obj) >= minimum:
                return False, _('must be at least {minimum}'), _msg_ctx
        return True
    return _validator


def length_max(maximum):
    return length(minimum=None, maximum=maximum)


def length_min(minimum):
    return length(minimum=minimum, maximum=None)


def type_(t):

    @true_if_empty
    @wraps(type_)
    def _validator(obj, selector, ctx):
        if not isinstance(obj, t):
            return False, _('Not a {type}'), {'type': t}
        return True
    return _validator


def _value(value, name, attrib, err_msg):

    @true_if_empty
    def _validator(obj, selector, ctx):
        if hasattr(obj, attrib):
            o = getattr(obj, attrib)
            if callable(o):
                result = o(value)
            else:
                result = (o == value)
            if result is not True:
                return False, err_msg, {'attrib': attrib, 'value': value, 'o': o, 'result': result}
            return True
        return False, '{} member missing: {}'.format(obj, attrib)

    _validator.__name__ = name
    return _validator

                
lt = partial(_value, name='lt', attrib='__lt__', err_msg='{selector} is not less then {value}.')
gt = partial(_value, name='gt', attrib='__gt__', err_msg='{selector} is not greater then {value}.')
eq = partial(_value, name='eq', attrib='__eq__', err_msg='{selector} is not equal to {value}.')
ne = partial(_value, name='ne', attrib='__ne__', err_msg='{selector} is equal to {value}.')
lte = partial(_value, name='lte', attrib='__le__', err_msg='{selector is not less or equal to {value}.')
gte = partial(_value, name='gte', attrib='__ge__', err_msg='{selector is not greater or equal to {value}.')
