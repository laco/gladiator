import gladiator as gl


valid_test_data = {
    'email': 'test@example.com',
    'pw': 'password123',
    'name': 'Test Username',
    'birth_year': 1984
}


def custom_validator(obj, ctx, selector):
    if 'custom_variable' in ctx:
        return True
    else:
        return False, ctx['_trans'].gettext('{selector} Custom Validator Error Str')


registration_form_validator = (
    ('email', gl.required, gl.format_email),
    ('pw', gl.required, gl.length_max(128)),
    ('name', gl.required, gl.type_(str)),
    ('birth_year', gl.required, gl.type_(int), gl.value_max(2014 - 18)),
    custom_validator,
)


def test_registration_form():
    assert gl.validate(
        valid_test_data,
        registration_form_validator,
        {'custom_variable': 'exists'})\
             .success is True
