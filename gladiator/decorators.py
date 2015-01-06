from functools import wraps
from inspect import signature, _empty, isclass, getmro
from .core import validate


def validate_fn(validator=None, on_failure=None, vctx=None):

    def decorator(fn):
        @wraps(fn)
        def inner_fn(*args, **kwargs):
            vresult = _validate_fn_params(fn, validator, vctx, *args, **kwargs)
            if vresult.success:
                return fn(*args, **kwargs)
            else:
                return _handle_on_failure(vresult, on_failure, fn, *args, **kwargs)
        return inner_fn
    return decorator


def _annotation_is_validator(param):
    return param.annotation is not _empty and \
        (callable(param.annotation) or isinstance(param.annotation, (tuple, list)))


def _validate_fn_params(fn, validator=None, vctx=None, *args, **kwargs):
    sig = signature(fn)
    ba = sig.bind(*args, **kwargs)
    va = []
    for param in sig.parameters.values():
        if param.name not in ba.arguments:
            ba.arguments[param.name] = param.default
        if _annotation_is_validator(param) and ba.arguments[param.name] != param.default:
            # validate only if called with not the default value
            va.append((
                param.name,  # selector
                param.annotation  # validation rules
            ))
    if validator is not None:
        va = va + list(validator)
    return validate(va, ba.arguments, ctx=vctx)


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
