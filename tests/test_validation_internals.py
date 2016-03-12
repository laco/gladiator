from gladiator import validate
from gladiator.commons import Success, Failure, Skip, ValidatorType


# Primitive validation test

def test_positive_result_from_bool_validation_ret_val():

    def test_validator(obj, selector, ctx):
        return True

    result = validate(test_validator, 'obj')
    assert isinstance(result, Success)
    assert result.error is None


def test_negative_result_from_bool_validation_ret_val():

    def test_validator(obj, selector, ctx):
        return False

    result = validate(test_validator, 'obj')
    assert isinstance(result, Failure)
    assert result.error == 'None'


def test_negative_result_from_bool_error_validation_ret_val():

    def test_validator(obj, selector, ctx):
        return False, 'error message'

    result = validate(test_validator, 'obj')
    assert isinstance(result, Failure)
    assert result.error == 'error message'


def test_negative_result_from_bool_error_format_validation_ret_val():

    def test_validator(obj, selector, ctx):
        return False, 'error {msg}', {'msg': 'message'}

    result = validate(test_validator, 'obj')
    assert isinstance(result, Failure)
    assert result.error == 'error message'


def test_same_result_from_validationresult_ret_val():

    for ret_cls in (Success, Failure, Skip):

        ret_val = ret_cls(
            type_=ValidatorType.primitive,
            validator=lambda obj, selector, ctx: True,
            obj='obj',
            selector='test_selector',
            result=ret_cls is Success,
            msg='message' if ret_cls is Failure else None,
            ctx={})

        def test_validator(obj, selector, ctx):
            return ret_val

        result = validate(test_validator, 'obj')
        assert isinstance(result, ret_cls)
        assert result is ret_val
