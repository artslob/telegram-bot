from unittest.mock import patch

import pytest

import api.weather.yandex as weather
from telegram.commands import execute_command


@pytest.mark.parametrize('txt', [None, '', 'start', 'ping', 'echo', 'test', 'some text'])
async def test_no_command(update_object, txt):
    send_message = await execute_command(123, update_object(txt))
    assert send_message.text == 'No such command'


@pytest.mark.parametrize('txt', ['/ping', '/ping 123', '/ping\n123', '/ping\t123'])
async def test_ping(update_object, txt):
    send_message = await execute_command(123, update_object(txt))
    assert send_message.text == 'pong!'


@pytest.mark.parametrize('txt', ['/echo', '/echo text', '/echo     text', '/echo\n\ttext\ntest\t'])
async def test_echo(update_object, txt):
    send_message = await execute_command(123, update_object(txt))
    assert send_message.text == update_object(txt).to_str()


@pytest.mark.parametrize('txt', ['/start', '/start text', '/start     text', '/start\n\ttext\ntest\t'])
async def test_start(update_object, txt):
    send_message = await execute_command(123, update_object(txt))
    assert send_message.text == '\n'.join(['Hello! I can process such commands:',
                                           '/start - print available commands',
                                           '/echo - print input telegram Update object',
                                           '/ping - check bot availability',
                                           '/weather - returns current weather in SPb'])


@pytest.mark.parametrize('txt', ['/weather', '/weather 123', '/weather\n123', '/weather\t123'])
async def test_weather(txt, yandex_weather_json, async_context_response, update_object, redis_fixture):
    with patch('aiohttp.request') as request_mock, \
            patch('telegram.commands.error_log') as log_mock:
        request_mock.return_value = async_context_response(200, yandex_weather_json)
        first_chars = 133
        result = (await execute_command(123, update_object(txt))).text
        assert result[:first_chars] == weather.YandexWeather.stringify(yandex_weather_json)[:first_chars]
        assert result.startswith('Detailed: https://yandex.ru/pogoda/')
        log_mock.exception.assert_not_called()
        await redis_fixture[1]


async def test_weather_key_error(update_object, redis_fixture):
    with patch('api.weather.yandex.YandexWeather.weather_description') as weather_mock, \
            patch('telegram.commands.error_log') as log_mock:
        weather_mock.side_effect = KeyError('some key error')
        error_result = (await execute_command(123, update_object('/weather'))).text
        assert error_result == 'Sorry. Something went wrong while parsing answer from API.'
        log_mock.exception.assert_called_once()
        await redis_fixture[1]


async def test_weather_bad_answer(update_object, redis_fixture, yandex_weather_json):
    yandex_weather_json.pop('info')
    with patch('api.weather.yandex.YandexWeather.get_weather') as weather_mock, \
            patch('telegram.commands.error_log') as log_mock:
        async def new_weather():
            return yandex_weather_json

        weather_mock.return_value = new_weather()
        error_result = (await execute_command(123, update_object('/weather'))).text
        assert error_result == 'Sorry. Something went wrong while parsing answer from API.'
        log_mock.exception.assert_called_once()
        await redis_fixture[1]


async def test_weather_bad_status(update_object, redis_fixture):
    with patch('api.weather.yandex.YandexWeather.weather_description') as weather_mock, \
            patch('telegram.commands.error_log') as log_mock:
        weather_mock.side_effect = weather.ForbiddenRequestError()
        error_result = (await execute_command(123, update_object('/weather'))).text
        assert error_result.startswith('Sorry. Error occurred during the request to API.')
        log_mock.exception.assert_called_once()
        await redis_fixture[1]
