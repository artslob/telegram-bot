import pytest

from telegram.objects import Message, Chat


@pytest.fixture()
def parse_message_dict(dict_parser):
    return dict_parser(Message)


def test_empty_dict(parse_message_dict):
    with pytest.raises(TypeError, match='missing 3 required positional arguments'):
        parse_message_dict({})


def test_message(parse_message_dict):
    message_dict = {
        "date": 1441645532,
        "chat": {
            "last_name": "Test Lastname",
            "type": "private",
            "id": 1111111,
            "first_name": "Test Firstname",
            "username": "Testusername"
        },
        "message_id": 1365,
        "from": {
            "last_name": "Test Lastname",
            "id": 1111111,
            "first_name": "Test Firstname",
            "username": "Testusername"
        },
        "text": "/start",
    }
    message = parse_message_dict(message_dict)
    assert message.message_id == 1365
    assert message.date == 1441645532
    assert type(message.chat) is Chat
    assert message.from_user is None  # FIXME
    assert message.text == '/start'
