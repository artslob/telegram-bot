from unittest.mock import patch

import pytest

import config
from telegram.methods import SetWebhookMethod, SendMessageMethod


@pytest.mark.parametrize('method', [SetWebhookMethod, SendMessageMethod])
def test_methods(method, monkeypatch):
    api = 'https://some_api.com'
    monkeypatch.setattr(config, 'API', api)

    with patch('aiohttp.request') as request_mock:
        dct = {'test': 'value'}
        method.post_json(dct)
        request_mock.assert_called_once()
        args, kwargs = request_mock.call_args
        assert args == ('POST',)
        assert kwargs['url'] == f'{api}/{method.method_address()}'
        assert kwargs['json'] is dct
        assert kwargs['headers'] == {'Content-Type': 'application/json'}
        assert kwargs['timeout'] is method.default_timeout
