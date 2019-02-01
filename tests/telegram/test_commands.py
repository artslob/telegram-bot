from unittest.mock import patch

import pytest

from api.weather.yandex import YandexWeather
from telegram.commands import execute_command


@pytest.mark.parametrize('txt', [None, '', 'start', 'ping', 'echo', 'test', 'some text'])
async def test_no_command(update_object, txt):
    assert await execute_command(update_object(txt)) == 'No such command'


@pytest.mark.parametrize('txt', ['/ping', '/ping 123', '/ping\n123', '/ping\t123'])
async def test_ping(update_object, txt):
    assert await execute_command(update_object(txt)) == 'pong!'


@pytest.mark.parametrize('txt', ['/echo', '/echo text', '/echo     text', '/echo\n\ttext\ntest\t'])
async def test_echo(update_object, txt):
    assert await execute_command(update_object(txt)) == update_object(txt).to_str()


@pytest.mark.parametrize('txt', ['/weather', '/weather 123', '/weather\n123', '/weather\t123'])
@pytest.mark.parametrize('error_status', [302, 400, 403, 500])
async def test_weather(txt, error_status, yandex_weather_json, async_context_response, update_object):
    with patch('aiohttp.request') as request_mock:
        request_mock.return_value = async_context_response(200, yandex_weather_json)
        assert await execute_command(update_object(txt)) == YandexWeather.stringify(yandex_weather_json)

        request_mock.return_value = async_context_response(error_status, yandex_weather_json)
        error_result = await execute_command(update_object(txt))
        assert error_result.startswith('Sorry. Error occurred during the request to API.')
