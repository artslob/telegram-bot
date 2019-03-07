from telegram.objects import SendMessageObject


def test_send_message():
    obj = SendMessageObject(123, 'some test')
    assert obj.chat_id == 123
    assert obj.text == 'some test'
    assert obj.parse_mode is None
    assert obj.disable_web_page_preview is None
    assert obj.disable_notification is None
    assert obj.reply_to_message_id is None
    assert obj.to_dict() == {'chat_id': 123, 'text': 'some test'}


def test_all_fields_initialised():
    obj = SendMessageObject(123, 'some test', 'markdown', True, True, 321)
    assert obj.chat_id == 123
    assert obj.text == 'some test'
    assert obj.parse_mode == 'markdown'
    assert obj.disable_web_page_preview is True
    assert obj.disable_notification is True
    assert obj.reply_to_message_id == 321
    assert obj.to_dict() == {
        'chat_id': 123, 'text': 'some test', 'parse_mode': 'markdown',
        'disable_web_page_preview': True, 'disable_notification': True, 'reply_to_message_id': 321
    }
