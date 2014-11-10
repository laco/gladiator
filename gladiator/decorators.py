from functools import wraps
from inspect import signature, _empty, isclass, getmro
from .core import validate


def validate_fn(validator=None, on_failure=None, ctx=None):

    def decorator(fn):
        @wraps(fn)
        def inner_fn(*args, **kwargs):
            vresult = _validate_fn_params(fn, validator, ctx, *args, **kwargs)
            if vresult.success:
                return fn(*args, **kwargs)
            else:
                return _handle_on_failure(vresult, on_failure, fn, *args, **kwargs)
        return inner_fn
    return decorator


def _annotation_is_validator(param):
    return param.annotation is not _empty and \
        (callable(param.annotation) or isinstance(param.annotation, (tuple, list)))


def _validate_fn_params(fn, validator=None, ctx=None, *args, **kwargs):
    sig = signature(fn)
    ba = sig.bind(*args, **kwargs)
    va = list(validator or [])
    for param in sig.parameters.values():
        if param.name not in ba.arguments:
            ba.arguments[param.name] = param.default
        if _annotation_is_validator(param):
            va.append((
                param.name,  # selector
                param.annotation  # validation rules
            ))
    return validate(va, ba.arguments, ctx=ctx)


def _handle_on_failure(vresult, on_failure, fn, *args, **kwargs):
    if isclass(on_failure):
        if Exception in getmro(on_failure):
            raise on_failure(vresult)
        else:
            return on_failure(vresult=vresult)
    elif callable(on_failure):
        return on_failure(vresult)
    elif on_failure is None:
        return fn(*args, **kwargs)
