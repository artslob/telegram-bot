from unittest.mock import patch

import pytest

import config
from bot import webhook_address, create_app


@pytest.fixture
def patch_config(monkeypatch):
    monkeypatch.setattr(config, 'API', 'http://127.0.0.1:15346/bot')
    monkeypatch.setattr(config, 'HOST', 'https://test-bot.test.ru')
    monkeypatch.setattr(config, 'TOKEN', '123456:ABC-DEF1234ghIkl-zyx57W2grab_some_beer')
    return config


@pytest.fixture
def test_update_object():
    return {
        "update_id": 10000,
        "message": {
            "message_id": 1365,
            "date": 1441645532,
            "chat": {
                "id": 1111111,
                "type": "private",
                "username": "Testusername",
                "first_name": "Test Firstname",
                "last_name": "Test Lastname",
            },
            "from": {
                "last_name": "Test Lastname",
                "id": 1111111,
                "first_name": "Test Firstname",
                "username": "Testusername",
                "is_bot": False,
            },
            "text": "/ping"
        }
    }


@pytest.mark.parametrize("text,answer", [
    ('/ping', 'pong!'),
    ('/echo 123 test', '/echo 123 test'),
    ('/echo      123 test', '/echo 123 test'),
])
async def test_webhook(text, answer, patch_config, aiohttp_client, async_context_response, test_update_object):
    test_update_object['message']['text'] = text
    assert webhook_address() == f'/{patch_config.TOKEN}'
    with patch('bot.logger') as logger_mock, \
            patch('bot.SendMessageMethod.post_json') as method_mock:
        method_mock.return_value = async_context_response(200, {})
        webhook = create_app()
        client = await aiohttp_client(webhook)
        resp = await client.post(webhook_address(), json=test_update_object)
        assert resp.status == 200
        assert await resp.text() == ''
        logger_mock.info.assert_called_once()
        logger_mock.exception.assert_not_called()
        method_mock.assert_called_once()
        expected_answer = {'chat_id': test_update_object['message']['chat']['id'], 'text': answer}
        assert method_mock.call_args[0][0] == expected_answer
