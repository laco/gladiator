from logging import getLogger
from gettext import NullTranslations


logger = getLogger(__name__)

# legyen beállíthato, hogy elso hibanal megalljon

default_validation_ctx = {
    '_trans': NullTranslations()
}


class ValidationResult(object):
    def __init__(self, obj, validator, ctx, selector, result, **kw):
        self.obj = obj
        self.validator = validator
        self.ctx = ctx
        self.selector = selector
        self.result = result
        self.kw = kw

    def __bool__(self):
        raise NotImplemented
    
    @property
    def success(self):
        return bool(self)
    
    @property
    def errors(self):
        if self.is_primitive():
            return self._primitive_errors()
        elif self.is_composite():
            return self._composite_errors()

    def is_primitive(self):
        return callable(self.validator)
    
    def is_composite(self):
        return isinstance(self.validator, (list, tuple))

    def _primitive_errors(self):
        if not self.success:
            return (self.selector, self.result.get(1, ''))

    def _composite_errors(self):
        if not self.sucess:
            return (self.selector, [r.errors for r in self.result])


class Success(ValidationResult):

    def __bool__(self):
        return True


class Failure(ValidationResult):

    def __bool__(self):
        return False


def validate(obj, validator, ctx=None, selector=None):
    ctx = ctx or default_validation_ctx.copy()
    selector = selector or []


    if callable(validator):
        return _primitive_validate(obj, validator, ctx, selector)
    elif isinstance(validator, (list, tuple)):
        return _composite_validate(obj, validator, ctx, selector)


def _primitive_validate(obj, validator, ctx, selector):
    print(selector, validator.__name__)
    result = validator(obj, ctx=ctx, selector=selector)
    ret_cls = Success if result is True else Failure
    return ret_cls(**locals())


def _composite_validate(obj, validator, ctx, selector):
    def _has_selector(validator):
        return len(validator) >= 1 and isinstance(validator[0], str)

    def _apply_selector(obj, selector):
        if isinstance(obj, dict):
            return obj.get(selector, None)
        else:
            return getattr(obj, selector, None)

    if _has_selector(validator):
        _selector, _validators = selector + [validator[0]], validator[1:]
        _obj = _apply_selector(obj, _selector[-1])
    else:
        _selector, _validators, _obj = selector, validator, obj
    result = [validate(_obj, v, ctx, _selector) for v in _validators]
    ret_cls = Success if all(result) else Failure
    
    return ret_cls(
        obj=_obj,
        validator=validator,
        ctx=ctx,
        result=result,
        selector=selector
    )
