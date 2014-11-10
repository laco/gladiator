import pytest

from gladiator.decorators import validate_fn
from gladiator.validators import required, type_, gt, length


user_dt = (
    ('_id', required, type_(int), gt(0)),
    ('name', required, type_(str), length(5, 16)))


client_dt = (
    ('_id', required, type_(int), gt(0)),
    ('user_ids', type_(list),
     ('@all', type_(int), gt(0))))

BAD_USER_PARAMETERS = [
    {'_id': -1, 'name': 'Test User'},
    {'_id': 2, 'name': 'Test User with tooo looong nameeeeee'},
    {'_id': 2, },
    None,
    {'some_random_key': 2, }
    
]

BAD_CLIENT_PARAMETERS = [
    {'_id': -1, 'user_ids': None},
    {'_id': 0, 'user_ids': []},
    {'_id': 1.2, 'user_ids': []},
    {'_id': '1', 'user_ids': []},
    {'user_ids': None},
]


@validate_fn(on_failure=ValueError)
def add_user_to_client(user: user_dt, client: client_dt):
    client.setdefault('user_ids', []).append(user['_id'])
    return client


def test_add_user_call_with_good_parameters():
    client = add_user_to_client({'_id': 1, 'name': 'Test User'}, client={'_id': 99, 'user_ids': []})
    assert 1 in client['user_ids']


def test_add_user_call_with_bad_user_parameter():
    for user_param in BAD_USER_PARAMETERS:
        with pytest.raises(ValueError):
            add_user_to_client(user_param, client={'_id': 99, 'user_ids': []})


def test_add_user_call_with_bad_client_parameters():
    for client_param in BAD_CLIENT_PARAMETERS:
        with pytest.raises(ValueError):
            add_user_to_client(user={'_id': 123, 'name': 'Good Name'}, client=client_param)


# Custom validators are great!
# This is one:


def validate_user_in_client(obj, selector, ctx):
    try:
        if obj['user']['_id'] in obj['client']['user_ids']:
            return True
    except KeyError:
        pass
    return False, 'User not in client!!!'


@validate_fn([validate_user_in_client], on_failure=ValueError)
def remove_user_from_client(user: user_dt, client: client_dt):
    client.setdefault('user_ids', []).remove(user['_id'])
    return client


def test_remove_user_call_with_empty_client():
    with pytest.raises(ValueError):
        remove_user_from_client(user={'_id': 122, 'name': 'Very Good Name'}, client={'_id': 111, 'user_ids': []})
