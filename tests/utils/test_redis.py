import importlib
import json
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

import api.weather.yandex.yandex as weather
from utils.redis import RedisDB, DatetimeDump


@pytest.fixture
async def redis_fixture(loop):
    redis = await RedisDB.create()
    await redis.flushdb()

    # should be awaited in test!
    async def fin():
        redis.close()
        await redis.wait_closed()
        RedisDB._redis = None

    return redis, fin()


async def test_redis_singleton(redis_fixture):
    assert await RedisDB.create() is await RedisDB.create()
    await redis_fixture[1]


async def test_set_get(redis_fixture):
    redis, fin = redis_fixture
    await redis.set('my-key', 'value')
    assert b'value' == await redis.get('my-key')
    await fin


async def test_1(redis_fixture):
    redis, fin = redis_fixture
    value = await redis.get('my-key')
    assert value is None
    await fin


async def test_store_api_dict(redis_fixture, yandex_weather_json):
    redis, fin = redis_fixture
    await redis.set('weather_json', json.dumps(yandex_weather_json))
    result = json.loads(await redis.get('weather_json'))
    assert result == yandex_weather_json
    await fin


async def test_datetime_dump(redis_fixture):
    redis, fin = redis_fixture
    now = datetime.now()
    await redis.set('datetime', DatetimeDump.dump(now))
    result = DatetimeDump.restore(await redis.get('datetime', encoding='utf-8'))
    assert now == result
    await fin


async def test_cached_api_call(redis_fixture, yandex_weather_json, async_context_response):
    """
    Test that first call to API produced, another after it is cached, third after some time is requested again
    """
    redis, fin = redis_fixture
    with patch('aiohttp.request') as request_mock, \
            patch('utils.redis.now_func') as now_mock:
        importlib.reload(weather)
        request_mock.return_value = async_context_response(200, yandex_weather_json)
        start_datetime = datetime(2019, 1, 1)
        now_mock.return_value = start_datetime
        time_key = 'api.weather.yandex.yandex/YandexWeather.get_weather/__time__'

        result = await weather.YandexWeather.get_weather()
        assert result['_cache_updated'] == DatetimeDump.dump(start_datetime)
        assert await redis.get(time_key, encoding='utf-8') == DatetimeDump.dump(start_datetime)
        request_mock.assert_called_once()

        result = await weather.YandexWeather.get_weather()
        assert result['_cache_updated'] == DatetimeDump.dump(start_datetime)
        assert await redis.get(time_key, encoding='utf-8') == DatetimeDump.dump(start_datetime)
        request_mock.assert_called_once()

        second_datetime = start_datetime + timedelta(minutes=30)
        now_mock.return_value = second_datetime
        result = await weather.YandexWeather.get_weather()
        assert result['_cache_updated'] == DatetimeDump.dump(second_datetime)
        assert await redis.get(time_key, encoding='utf-8') == DatetimeDump.dump(second_datetime)
        assert request_mock.call_count == 2

        await fin


async def test_cached_api_call_in_database(redis_fixture, yandex_weather_json, async_context_response):
    """
    Test that when values exist in database no call to API is produced
    """
    redis, fin = redis_fixture
    with patch('aiohttp.request') as request_mock, \
            patch('utils.redis.now_func') as now_mock:
        importlib.reload(weather)
        request_mock.return_value = async_context_response(200, yandex_weather_json)
        start_datetime = datetime(2019, 1, 1)
        now_mock.return_value = start_datetime
        time_key = 'api.weather.yandex.yandex/YandexWeather.get_weather/__time__'
        value_key = 'api.weather.yandex.yandex/YandexWeather.get_weather/__value__'
        await redis.set(time_key, DatetimeDump.dump(start_datetime))
        await redis.set(value_key, json.dumps(yandex_weather_json))

        result = await weather.YandexWeather.get_weather()
        assert '_cache_updated' not in result
        assert await redis.get(time_key, encoding='utf-8') == DatetimeDump.dump(start_datetime)
        request_mock.assert_not_called()

        await fin


async def test_cached_api_call_in_database_expired(redis_fixture, yandex_weather_json, async_context_response):
    """
    Test that when values exist in database but expired, new call is produced
    """
    redis, fin = redis_fixture
    with patch('aiohttp.request') as request_mock, \
            patch('utils.redis.now_func') as now_mock:
        importlib.reload(weather)
        request_mock.return_value = async_context_response(200, yandex_weather_json)
        start_datetime = datetime(2019, 1, 1)
        now_mock.return_value = start_datetime
        time_key = 'api.weather.yandex.yandex/YandexWeather.get_weather/__time__'
        value_key = 'api.weather.yandex.yandex/YandexWeather.get_weather/__value__'
        await redis.set(time_key, DatetimeDump.dump(start_datetime - timedelta(minutes=30)))
        assert await redis.get(value_key, encoding='utf-8') is None

        result = await weather.YandexWeather.get_weather()
        assert result['_cache_updated'] == DatetimeDump.dump(start_datetime)
        assert await redis.get(time_key, encoding='utf-8') == DatetimeDump.dump(start_datetime)
        assert await redis.get(value_key, encoding='utf-8') == json.dumps(yandex_weather_json)
        request_mock.assert_called_once()

        await fin
