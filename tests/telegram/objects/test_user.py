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
    chat = parse_user_dict(user_dict)
    assert chat.to_dict() == user_dict
    assert chat.id == 1111111
    assert chat.is_bot is False
    assert chat.first_name == 'Test Firstname'
    assert chat.language_code == 'us'
    assert chat.last_name == 'Test Lastname'
    assert chat.username == 'Testusername'
