import pytest

from telegram.objects import Chat


@pytest.fixture()
def parse_chat_dict(dict_parser):
    return dict_parser(Chat)


def test_empty_dict(parse_chat_dict):
    with pytest.raises(TypeError, match='missing 2 required positional arguments'):
        parse_chat_dict({})


def test_chat(parse_chat_dict):
    chat_dict = {
        "id": 1111111,
        "type": "private",
        "username": "Testusername",
        "first_name": "Test Firstname",
        "last_name": "Test Lastname",
        "all_members_are_administrators": True,
        "description": "test description",
        "invite_link": "t.me/test",
        "pinned_message": {
            "date": 1441645532,
            "chat": {
                "last_name": "Test Lastname",
                "type": "private",
                "id": 1111111,
                "first_name": "Test Firstname",
                "username": "Testusername"
            },
            "message_id": 1365,
        },
        "sticker_set_name": 'sticker test',
        "can_set_sticker_set": True,
    }
    chat = parse_chat_dict(chat_dict)
    assert chat.id == 1111111
    assert chat.type == 'private'
    assert chat.username == 'Testusername'
    assert chat.first_name == 'Test Firstname'
    assert chat.last_name == 'Test Lastname'
    assert chat.all_members_are_administrators is True
    assert chat.description == 'test description'
    assert chat.invite_link == "t.me/test"
    assert chat.pinned_message.message_id == 1365
    assert chat.pinned_message.date == 1441645532
    assert chat.pinned_message.chat is not None
    assert chat.pinned_message.chat.id == 1111111
    assert chat.pinned_message.chat.type == 'private'
    assert chat.pinned_message.chat.username == 'Testusername'
    assert chat.pinned_message.chat.first_name == 'Test Firstname'
    assert chat.pinned_message.chat.last_name == 'Test Lastname'
    assert chat.sticker_set_name == 'sticker test'
    assert chat.can_set_sticker_set is True
