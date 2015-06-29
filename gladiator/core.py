import logging
import sys
from uuid import uuid4
from gettext import NullTranslations
from .utils import selector_as_string
from .commons import ValidatorType, Success, Failure, Skip


# logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)


default_validation_ctx = {
    'lazy': True,
    'validation_failed': False,
    'trans': NullTranslations(),
    'err_msgs': {
    }
}


def validate(validator, obj, selector=None, ctx=None, **kw):
    ctx = _init_once_ctx(ctx, obj, **kw)

    selector = selector or []
    type_ = _detect_validator_type(validator)

    if _lazy_and_already_failed(ctx, selector, validator):
        result = _skip_validate(validator, obj, selector, ctx)
    elif type_ == ValidatorType.primitive:
        result = _primitive_validate(validator, obj, selector, ctx)
    elif type_ == ValidatorType.composite:
        result = _composite_validate(validator, obj, selector, ctx)

    if result.success is False and type_ == ValidatorType.primitive:
        _lazy_register_failed(ctx, selector)

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(' {id} {vname} on object {obj} (selector={selector}) result: {result}'.format(
            id=ctx['uuid'],
            vname=validator.__name__ if type_ == ValidatorType.primitive else 'composite-{}'.format(id(validator)),
            obj=str(obj),
            selector=selector_as_string(selector),
            result=result.__class__.__name__
        ))
    return result


def _lazy_and_already_failed(ctx, selector, validator):
    return (ctx.get('lazy', True) and
            (
                (selector_as_string(selector) in ctx.get('_failed_selectors', [])) or
                (getattr(validator, '_lazy', False) and ctx.get('validation_failed', False))))


def _lazy_register_failed(ctx, selector):
    ctx['validation_failed'] = True
    if selector not in ctx.get('_failed_selectors', []):
        ctx.setdefault('_failed_selectors', []).append(selector_as_string(selector))


def _init_once_ctx(ctx, obj, **kw):
    if ctx is None or ctx.get('__initialized', None) is None:
        _ctx = default_validation_ctx.copy()
        _ctx.update(ctx or {})
        _ctx.update(kw)
        _ctx.setdefault('uuid', uuid4().hex)
        _ctx.setdefault('initial_obj', obj)
        _ctx['__initialized'] = True
        return _ctx
    else:
        return ctx


def _detect_validator_type(validator):
    if callable(validator):
        return ValidatorType.primitive
    elif isinstance(validator, (list, tuple)):
        return ValidatorType.composite
    else:
        return ValidatorType.unknown


def _skip_validate(validator, obj, selector, ctx):
    return Skip(
        type_=_detect_validator_type(validator),
        validator=validator,
        obj=obj,
        selector=selector,
        ctx=ctx)


def _primitive_validate(validator, obj, selector, ctx):

    def _parse_primitive_validator_ret(ret_):
        if isinstance(ret_, tuple):
            if len(ret_) == 2:
                result, msg, msg_ctx = ret_[0], ret_[1], {}
            elif len(ret_) == 3:
                result, msg, msg_ctx = ret_
        elif isinstance(ret_, bool):
            result, msg, msg_ctx = ret_, None, {}
        return result, msg, msg_ctx

    _ret = validator(obj, selector=selector, ctx=ctx)
    result, msg, msg_ctx = _parse_primitive_validator_ret(_ret)
    ret_cls = Success if result is True else Failure
    return ret_cls(
        type_=ValidatorType.primitive,
        validator=validator,
        obj=obj,
        selector=selector,
        ctx=ctx,
        result=result,
        msg=msg,
        msg_ctx=msg_ctx)


def _composite_validate(validator, obj, selector, ctx):
    def _has_selector(validator):
        return len(validator) >= 1 and isinstance(validator[0], (str, int))

    def _apply_selector(obj, selector_str, current_selector):
        if selector_str in ctx.get('custom_selectors', {}):
            return ctx['custom_selectors'][selector_str](obj, current_selector)
        elif isinstance(selector_str, int) and isinstance(obj, (tuple, list)):
            try:
                new_obj = obj[selector_str]
            except IndexError:
                new_obj = None
            return [(current_selector + [str(selector_str)], new_obj)]

        elif selector_str == '@all':
            return [(current_selector + [index], value) for index, value in enumerate(obj or [])]
        elif selector_str == '@first':
            ret_selector = current_selector + [0]
            return [(ret_selector, next(iter(obj), None))]
        elif isinstance(obj, dict):
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
        type_=ValidatorType.composite,
        validator=validator,
        obj=obj,
        selector=selector,
        ctx=ctx,
        results=results,
    )
