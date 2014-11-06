from .utils import selector_as_string


class ValidatorType(object):
    primitive = 'primitive'
    composite = 'composite'
    unknown = 'unknown'


class ValidationResult(object):
    def __init__(self, type_, validator, obj, selector, ctx, **kw):
        self.type_ = type_
        self.validator = validator
        self.obj = obj
        self.selector = selector
        self.ctx = ctx
        if type_ == 'primitive':
            self.result = kw.pop('result', None)
            self.msg = kw.pop('msg', None)
            self.msg_ctx = kw.pop('msg_ctx', {})
        elif type_ == 'composite':
            self.results = kw.pop('results', [])
        self.kw = kw

    def __nonzero__(self):
        return self.__bool__()

    def __bool__(self):
        raise NotImplemented
    
    @property
    def success(self):
        return bool(self)

    @property
    def error(self):
        if self.type_ == 'primitive' and not self.success:
            return self._error_msg()

    @property
    def errors(self):
        if self.type_ == 'composite':
            if not self.success:
                return self._error_list()
            else:
                return []

    def _error_msg(self):
        _ctx = {
            'selector': selector_as_string(self.selector),
        }
        gettext = self.ctx['trans'].gettext
        _ctx.update(self.ctx)
        _ctx.update(self.msg_ctx)
        return str(gettext(self.msg)).format(**_ctx)

    def _error_list(self):
        err_list = []
        for r in self.results:
            if not r.success and isinstance(r, Failure):
                if r.type_ == ValidatorType.primitive:
                    err_list.append((selector_as_string(r.selector), r.error))
                elif r.type_ == ValidatorType.composite:
                    err_list += r._error_list()
        return err_list
        
    def __repr__(self):
        if self.type_ == ValidatorType.primitive:
            return "{0}[{1}]".format(
                self.__class__.__name__,
                selector_as_string(self.selector))
        elif self.type_ == ValidatorType.composite:
            return '{0}({1}{2})'.format(
                self.__class__.__name__,
                '',
                ', '.join([repr(r) for r in self.results]))


class Success(ValidationResult):

    def __bool__(self):
        return True


class Failure(ValidationResult):

    def __bool__(self):
        return False


class Skip(ValidationResult):

    def __bool__(self):
        return False
