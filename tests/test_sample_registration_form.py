import gladiator as gl
from functools import partial


def _(msg):
    return msg


valid_test_data = {
    'email': 'test@example.com',
    'pw': 'password123',
    'name': 'Test Username',
    'birth_year': 1984
}


invalid_test_data = {
    'email': 'missingatcharacter.com',
    'pw': '',
    'name': 'Test Username',
    'birth_year': 'not number!!!'
}


def custom_validator(obj, selector, ctx):
    if 'custom_variable' in ctx:
        return True
    else:
        return False, _('{selector} Custom Validator Error Str')


registration_form_validator = (
    ('email', gl.required, gl.format_email),
    ('pw', gl.required, gl.length_min(5)),
    ('name', gl.required, gl.type_(str)),
    ('birth_year', gl.required, gl.type_(int), gl.lt((2014 - 18))),
    custom_validator,
)


def test_registration_form():
    validator_func = partial(gl.validate, registration_form_validator, ctx={'custom_variable': 'exists', 'lazy': True})
    
    success_result = validator_func(valid_test_data)
    failure_result = validator_func(invalid_test_data)
    
    assert success_result.success is True
    assert success_result.errors == []
    assert failure_result.success is False
    assert len(failure_result.errors) == 3  # lazyness!!
