import gladiator as gl

valid_test_data = {
    'cart_id': 123,
    'user_id': 1,
    'items': [
        {'item_id': 1, 'price': 1.34, 'count': 1},
        {'item_id': 2, 'price': 0.34, 'count': 2},
        {'item_id': 3, 'price': 1.22, 'count': 1},
    ]
}


validation_rules = (
    ('cart_id', gl.required, gl.type_(int)),
    ('user_id', gl.required, gl.type_(int)),
    ('items', gl.type_(list),
     ('@all',
      ('item_id', gl.required),
      ('price', gl.required, gl.type_(float)),
      ('count', gl.required, gl.type_(int)))))


def test_shopping_cart_with_valid_data():
    result = gl.validate(validation_rules, valid_test_data)
    assert result.success is True


def test_shopping_cart_with_empty_data():
    result = gl.validate(validation_rules, {})
    assert result.success is False
