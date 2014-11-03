from functools import wraps, partial
from .utils import dummy_gettext as _


FALSE_VALUES = (None, '', 0, False)


def required(obj, **kw):
    return (False, _('missing value.')) if obj in FALSE_VALUES else True


def format_email(obj, **kw):
    return (False, _('bad email format')) if '@' not in obj else True


def length(minimum, maximum):
    _msg_ctx = {
        'minimum': minimum,
        'maximum': maximum
    }

    @wraps(length)
    def _validator(obj, selector, ctx):
        if minimum is not None and maximum is not None:
            if not len(obj) >= minimum and len(obj) <= maximum:
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


# def length_max(l):
#     @wraps(length_max)
#     def _validator(obj, ctx, **kw):
#         if len(obj) <= l:
#             return True
#         else:
#             return False,\
#                 get_error_msg(
#                     ctx,
#                     'length_max',
#                     'Value is to long.',
#                     length=l)
                
#     return _validator


def type_(t):
    @wraps(type_)
    def _validator(obj, ctx, **kw):
        if not isinstance(obj, t):
            return False, _('Not a {type}'), {'type': t}
        return True
    return _validator


def value_max(v):
    @wraps(value_max)
    def _validator(obj, ctx, **kw):
        try:
            if obj <= v:
                return True
            else:
                return False, 'Max value Error'
        except TypeError as e:
            return False, str(e)
    return _validator
