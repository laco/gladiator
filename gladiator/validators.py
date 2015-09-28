import re
from functools import wraps, partial
from .utils import dummy_gettext as _


FALSE_VALUES = (None, '')


def true_if_empty(func):
    """If you put this decorator on a validator
    the validator never fail if tho value is missing.
    
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


def skip_on_fail(func):
    func._lazy = True
    return func


def required(obj, selector, ctx):
    return (False, _('missing value.')) if obj in FALSE_VALUES else True


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
            return False, _('Object {otype} is not a {type}'), {'type': t, 'otype': type(obj)}
        return True
    return _validator


def regex_(pattern, pattern_name=None):
    if isinstance(pattern, str):
        _pattern = re.compile(pattern)
    else:
        _pattern = pattern

    @true_if_empty
    @wraps(regex_)
    def _validator(obj, selector, ctx):
        if _pattern.fullmatch(obj):
            return True
        return False, _('Value not match {pattern_name} format.'), {'pattern': pattern, 'pattern_name': pattern_name or pattern}
    return _validator


def _value(value, name, attrib, err_msg):

    @true_if_empty
    @wraps(_value)
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


def in_(lst):
    
    lst = lst or []

    @true_if_empty
    @wraps(in_)
    def _validator(obj, selector, ctx):
        return True if obj in lst else False, _('{obj} not in options: {lst}'), {'lst': lst, 'obj': obj}
    return _validator


# email regex rules
WSP = r'[ \t]'                                       # see 2.2.2. Structured Header Field Bodies
CRLF = r'(?:\r\n)'                                   # see 2.2.3. Long Header Fields
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'        # see 3.2.1. Primitive Tokens
QUOTED_PAIR = r'(?:\\.)'                             # see 3.2.2. Quoted characters
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + \
    WSP + r'+)'                                    # see 3.2.3. Folding white space and comments
CTEXT = r'[' + NO_WS_CTL + \
    r'\x21-\x27\x2a-\x5b\x5d-\x7e]'              # see 3.2.3
CCONTENT = r'(?:' + CTEXT + r'|' + \
    QUOTED_PAIR + r')'                        # see 3.2.3 (NB: The RFC includes COMMENT here
# as well, but that would be circular.)
COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \
    r')*' + FWS + r'?\)'                       # see 3.2.3
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + \
    FWS + '?' + COMMENT + '|' + FWS + ')'         # see 3.2.3
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'            # see 3.2.4. Atom
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'       # see 3.2.4
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'    # see 3.2.4
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?'  # see 3.2.4
QTEXT = r'[' + NO_WS_CTL + \
    r'\x21\x23-\x5b\x5d-\x7e]'                   # see 3.2.5. Quoted strings
QCONTENT = r'(?:' + QTEXT + r'|' + \
    QUOTED_PAIR + r')'                        # see 3.2.5
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
    r'?' + QCONTENT + r')*' + FWS + \
    r'?' + r'"' + CFWS + r'?'
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
    QUOTED_STRING + r')'                    # see 3.4.1. Addr-spec specification
DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'    # see 3.4.1
DCONTENT = r'(?:' + DTEXT + r'|' + \
    QUOTED_PAIR + r')'                        # see 3.4.1
DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \
    r'(?:' + FWS + r'?' + DCONTENT + \
    r')*' + FWS + r'?\]' + CFWS + r'?'  # see 3.4.1
DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
    DOMAIN_LITERAL + r')'                       # see 3.4.1
ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN               # see 3.4.1
VALID_ADDRESS_REGEXP = re.compile('^' + ADDR_SPEC + '$')
format_email = regex_(VALID_ADDRESS_REGEXP, 'email')


lt = partial(_value, name='lt', attrib='__lt__', err_msg='{selector} is not less then {value}.')
gt = partial(_value, name='gt', attrib='__gt__', err_msg='{selector} is not greater then {value}.')
eq = partial(_value, name='eq', attrib='__eq__', err_msg='{selector} is not equal to {value}.')
ne = partial(_value, name='ne', attrib='__ne__', err_msg='{selector} is equal to {value}.')
lte = partial(_value, name='lte', attrib='__le__', err_msg='{selector is not less or equal to {value}.')
gte = partial(_value, name='gte', attrib='__ge__', err_msg='{selector is not greater or equal to {value}.')
