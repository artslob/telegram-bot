from unittest.mock import patch

import pytest

from api.weather.yandex import YandexWeather
from telegram.commands import execute_command
from telegram.objects import Update


@pytest.fixture
def update_object():
    def get_object(text):
        return Update.from_dict({
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
                "text": text
            },
        })

    return get_object


@pytest.mark.parametrize('txt', [None, '', 'start', 'ping', 'echo', 'test', 'some text'])
async def test_no_command(update_object, txt):
    assert await execute_command(update_object(txt)) == 'No such command'


@pytest.mark.parametrize('txt', ['/ping', '/ping 123', '/ping\n123', '/ping\t123'])
async def test_ping(update_object, txt):
    assert await execute_command(update_object(txt)) == 'pong!'


@pytest.mark.parametrize('txt, expected', [
    ('/echo', '/echo '),
    ('/echo text', '/echo text'),
    ('/echo     text', '/echo text'),
    ('/echo\n\ttext\ntest\t', '/echo text test'),
])
async def test_echo(update_object, txt, expected):
    # TODO fix echo command
    assert await execute_command(update_object(txt)) == expected


@pytest.mark.parametrize('txt', ['/weather', '/weather 123', '/weather\n123', '/weather\t123'])
@pytest.mark.parametrize('error_status', [302, 400, 403, 500])
async def test_weather(txt, error_status, yandex_weather_json, async_context_response, update_object):
    with patch('aiohttp.request') as request_mock:
        request_mock.return_value = async_context_response(200, yandex_weather_json)
        assert await execute_command(update_object(txt)) == YandexWeather.stringify(yandex_weather_json)

        request_mock.return_value = async_context_response(error_status, yandex_weather_json)
        error_result = await execute_command(update_object(txt))
        assert error_result.startswith('Sorry. Error occurred during the request to API.')
