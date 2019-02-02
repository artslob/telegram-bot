import pytest

from telegram.objects import User


@pytest.fixture()
def parse_user_dict(dict_parser):
    return dict_parser(User)


def test_empty_dict(parse_user_dict):
    with pytest.raises(TypeError, match='missing 3 required positional arguments'):
        parse_user_dict({})


def test_user(parse_user_dict):
    user_dict = {
        "id": 1111111,
        "is_bot": False,
        "first_name": "Test Firstname",
        "language_code": "us",
        "last_name": "Test Lastname",
        "username": "Testusername"
    }
    user = parse_user_dict(user_dict)
    assert user.to_dict() == user_dict
    assert user.id == 1111111
    assert user.is_bot is False
    assert user.first_name == 'Test Firstname'
    assert user.language_code == 'us'
    assert user.last_name == 'Test Lastname'
    assert user.username == 'Testusername'
