from unittest.mock import patch

import pytest

from api.weather.yandex import YandexWeather
from telegram.commands import execute_command


@pytest.mark.parametrize('txt', [None, '', 'start', 'ping', 'echo', 'test', 'some text'])
async def test_no_command(txt):
    assert await execute_command(txt) == 'No such command'


@pytest.mark.parametrize('txt', ['/ping', '/ping 123', '/ping\n123', '/ping\t123'])
async def test_ping(txt):
    assert await execute_command(txt) == 'pong!'


@pytest.mark.parametrize('txt, expected', [
    ('/echo', '/echo '),
    ('/echo text', '/echo text'),
    ('/echo     text', '/echo text'),
    ('/echo\n\ttext\ntest\t', '/echo text test'),
])
async def test_echo(txt, expected):
    # TODO fix echo command
    assert await execute_command(txt) == expected


@pytest.mark.parametrize('txt', ['/weather', '/weather 123', '/weather\n123', '/weather\t123'])
@pytest.mark.parametrize('error_status', [302, 400, 403, 500])
async def test_weather(txt, error_status, yandex_weather_json, async_context_response):
    with patch('aiohttp.request') as request_mock:
        request_mock.return_value = async_context_response(200, yandex_weather_json)
        assert await execute_command(txt) == YandexWeather.stringify(yandex_weather_json)

        request_mock.return_value = async_context_response(error_status, yandex_weather_json)
        assert (await execute_command(txt)).startswith('Sorry. Error occurred during the request to API.')
