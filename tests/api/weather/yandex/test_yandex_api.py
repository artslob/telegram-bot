from unittest.mock import patch

import pytest

from api.weather.yandex import YandexWeather, ForbiddenRequestError, UnknownRequestError


async def test_successful_request(async_context_response):
    with patch('aiohttp.request') as request_mock:
        result = {'test': 123}
        request_mock.return_value = async_context_response(200, result)
        dct = await YandexWeather.get_weather.__wrapped__()
        assert dct == result


async def test_403(async_context_response):
    with patch('aiohttp.request') as request_mock:
        request_mock.return_value = async_context_response(403, {})
        with pytest.raises(ForbiddenRequestError):
            await YandexWeather.get_weather.__wrapped__()


@pytest.mark.parametrize('status', [301, 303, 400, 401, 500])
async def test_unexpected_status(status, async_context_response):
    with patch('aiohttp.request') as request_mock:
        request_mock.return_value = async_context_response(status, {})
        with pytest.raises(UnknownRequestError):
            await YandexWeather.get_weather.__wrapped__()
