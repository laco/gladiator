from functools import wraps


FALSE_VALUES = (None, '', 0, False)


def required(obj, **kw):
    return obj not in FALSE_VALUES


def format_email(obj, **kw):
    return '@' in obj


def length_max(l):
    @wraps(length_max)
    def _validator(obj, ctx, **kw):
        if len(obj) <= l:
            return True
        else:
            return False, 'Max length Error'
    return _validator


def type_(t):
    @wraps(type_)
    def _validator(obj, ctx, **kw):
        return isinstance(obj, t)
    return _validator


def value_max(v):
    @wraps(value_max)
    def _validator(obj, ctx, **kw):
        if obj <= v:
            return True
        else:
            return False, 'Max length Error'
    return _validator
