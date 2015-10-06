import gladiator as gl


#
# Comparison validators
#

comparison_validators_test_data = [
    {
        'validator': gl.lt(5),
        'valid': [1, 2, 3, 4],
        'invalid': [5, 6, 7, 8, 9, 10],
        'error': 'is not less then'
    },
    {
        'validator': gl.gt(5),
        'valid': [6, 7, 8, 9, 10],
        'invalid': [1, 2, 3, 4, 5],
        'error': 'is not greater then'
    },
    {
        'validator': gl.eq(5),
        'valid': [5],
        'invalid': [1, 2, 3, 4, 6, 7, 8, 9, 10],
        'error': 'is not equal to'
    },
    {
        'validator': gl.ne(5),
        'valid': [1, 2, 3, 4, 6, 7, 8, 9, 10],
        'invalid': [5],
        'error': 'is equal to'
    },
    {
        'validator': gl.lte(5),
        'valid': [1, 2, 3, 4, 5],
        'invalid': [6, 7, 8, 9, 10],
        'error': 'is not less or equal to'
    },
    {
        'validator': gl.gte(5),
        'valid': [5, 6, 7, 8, 9, 10],
        'invalid': [1, 2, 3, 4],
        'error': 'is not greater or equal to'
    }
]


def _yield_test_data(value_type):
    for validator_data in comparison_validators_test_data:
        validator = validator_data['validator']
        error = validator_data['error']
        for value in validator_data[value_type]:
            yield \
                (('test_field', validator),), \
                {'test_field': value}, \
                error


def test_comparison_operators_with_valid_values():
    for validation_rules, test_object, _ in _yield_test_data('valid'):
        result = gl.validate(validation_rules, test_object)
        assert result.success is True


def test_comparison_operators_with_invalid_values():
    for validation_rules, test_object, error in _yield_test_data('invalid'):
        result = gl.validate(validation_rules, test_object)
        assert result.success is False
        assert error in result.errors[0][1]
