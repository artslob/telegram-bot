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


@pytest.mark.parametrize('status', [200, 403, 500])
async def test_webhook(status, patch_config, aiohttp_client, async_context_response, update_dict):
    assert webhook_address() == f'/{patch_config.TOKEN}'
    with patch('bot.logger') as logger_mock, \
            patch('bot.SendMessageMethod.post_json') as method_mock:
        method_mock.return_value = async_context_response(status, {})
        webhook = create_app()
        client = await aiohttp_client(webhook)
        resp = await client.post(webhook_address(), json=update_dict('/ping'))
        assert resp.status == 200
        assert await resp.text() == ''
        logger_mock.info.assert_called_once()
        logger_mock.exception.assert_not_called()
        method_mock.assert_called_once()
        expected_answer = {'chat_id': update_dict('/ping')['message']['chat']['id'], 'text': 'pong!'}
        assert method_mock.call_args[0][0] == expected_answer
        if status == 200:
            logger_mock.error.assert_not_called()
        else:
            logger_mock.error.assert_called_once()
