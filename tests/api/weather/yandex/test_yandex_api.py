from unittest.mock import patch

import pytest

from api.weather.yandex import YandexWeather, ForbiddenRequestError, UnknownRequestError


@pytest.fixture
def async_context():
    class Response:
        def __init__(self, status, result):
            self.status = status
            self.result = result

        async def json(self):
            return self.result

    def context_manager_factory(status: int, result: dict):
        class ContextManager:
            async def __aenter__(self):
                return Response(status, result)

            async def __aexit__(self, *args, **kwargs):
                pass

        return ContextManager()

    return context_manager_factory


async def test_successful_request(async_context):
    with patch('aiohttp.request') as request_mock:
        result = {'test': 123}
        request_mock.return_value = async_context(200, result)
        dct = await YandexWeather.get_weather()
        assert dct == result


async def test_403(async_context):
    with patch('aiohttp.request') as request_mock:
        request_mock.return_value = async_context(403, {})
        with pytest.raises(ForbiddenRequestError):
            await YandexWeather.get_weather()


@pytest.mark.parametrize('status', [301, 303, 400, 401, 500])
async def test_unexpected_status(status, async_context):
    with patch('aiohttp.request') as request_mock:
        request_mock.return_value = async_context(status, {})
        with pytest.raises(UnknownRequestError):
            await YandexWeather.get_weather()
