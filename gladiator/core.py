from logging import getLogger
from gettext import NullTranslations

from .commons import Success, Failure


logger = getLogger(__name__)


default_validation_ctx = {
    'trans': NullTranslations(),
    'err_msgs': {
    }
}


def validate(validator, obj, selector=None, ctx=None):
    ctx = ctx or default_validation_ctx.copy()
    selector = selector or []

    if callable(validator):
        return _primitive_validate(validator, obj, selector, ctx)
    elif isinstance(validator, (list, tuple)):
        return _composite_validate(validator, obj, selector, ctx)


def _primitive_validate(validator, obj, selector, ctx):
    _ret = validator(obj, selector=selector, ctx=ctx)
    result, msg, msg_ctx = _parse_primitive_validator_ret(_ret)
    ret_cls = Success if result is True else Failure
    return ret_cls(
        type_='primitive',
        validator=validator,
        obj=obj,
        selector=selector,
        ctx=ctx,
        result=result,
        msg=msg,
        msg_ctx=msg_ctx)


def _parse_primitive_validator_ret(ret_):
    if isinstance(ret_, tuple):
        if len(ret_) == 2:
            result, msg, msg_ctx = ret_[0], ret_[1], {}
        elif len(ret_) == 3:
            result, msg, msg_ctx = ret_
    elif isinstance(ret_, bool):
        result, msg, msg_ctx = ret_, None, {}
    return result, msg, msg_ctx


def _composite_validate(validator, obj, selector, ctx):
    def _has_selector(validator):
        return len(validator) >= 1 and isinstance(validator[0], str)

    def _apply_selector(obj, selector_str, current_selector):
        if isinstance(obj, dict):
            return [(current_selector + [selector_str], obj.get(selector_str, None))]
        else:
            return [(current_selector + [selector_str], getattr(obj, selector_str, None))]
    
    if _has_selector(validator):
        results = [
            validate(v, _obj, _selector, ctx)
            for v in validator[1:]
            for _selector, _obj in _apply_selector(obj, validator[0], selector)
        ]
    else:
        results = [validate(v, obj, selector, ctx) for v in validator]
    
    ret_cls = Success if all(results) else Failure
    return ret_cls(
        type_='composite',
        validator=validator,
        obj=obj,
        selector=selector,
        ctx=ctx,
        results=results,
    )
