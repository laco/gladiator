from gladiator import validate


def always_true(obj, ctx, **kw):
    return True


def always_false(obj, ctx, **kw):
    return False, 'This is the error msg.'


def not_none(obj, ctx, **kw):
    return obj is not None


def is_none(obj, ctx, **kw):
    return not not_none(obj, ctx, **kw)


def test_simple_composition():
    test_obj = {
        'key1': 'value1',
        'key2': 'value2'
    }

    success_result = validate(
        [('key1', always_true),
         ('key2', always_true)], test_obj
    )
    failure_result = validate(
        [('key1', always_true),
         ('key2', always_false)], test_obj
    )
    assert bool(success_result) is True
    assert bool(failure_result) is False


def test_multilevel_composition():
    test_obj = {
        'key1': 'value1',
        'key2': 'value2'
    }

    success1_result = validate(
        [
            ('key1', always_true),
            always_true,
            ('key2', always_true),
            always_true
        ], test_obj)

    success2_result = validate(
        [
            ('key1', always_true, ('nested_key', always_true, always_true)),
            ('key2', always_true),
            always_true
        ], test_obj)

    assert bool(success1_result) is True
    assert bool(success2_result) is True


def test_values_exists():
    test_obj = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': None
    }
    result = validate(
        (('key1', not_none), ('key2', not_none), ('key3', is_none)), test_obj)
    assert bool(result) is True
