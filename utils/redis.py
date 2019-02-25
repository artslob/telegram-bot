import json
from datetime import timedelta, datetime
from functools import wraps
from inspect import signature, iscoroutinefunction

import aioredis

import config

now_func = datetime.now


class RedisDB:
    _redis: aioredis.Redis = None

    @classmethod
    async def create(cls):
        if cls._redis is None:
            cls._redis = await aioredis.create_redis_pool(f'redis://{config.REDIS_HOST}')

        return cls._redis


class DatetimeDump:
    date_fmt = '%Y-%m-%d %H:%M:%S.%f'

    @classmethod
    def dump(cls, value: datetime) -> str:
        return value.strftime(cls.date_fmt)

    @classmethod
    def restore(cls, value: str) -> datetime:
        return datetime.strptime(value, cls.date_fmt)


def redis_cache(calls_per_date: int):
    if calls_per_date <= 0:
        raise ValueError('calls per day should be positive number')

    delta = timedelta(days=1) / calls_per_date

    def decorator(func):
        if signature(func).parameters:
            raise TypeError('this decorator accepts functions without parameters')
        if not iscoroutinefunction(func):
            raise TypeError('decorated function should be coroutine')

        # get unique keys to store values
        key = f'{func.__module__}/{func.__qualname__}'
        value_key = f'{key}/__value__'
        time_key = f'{key}/__time__'

        last_accessed: datetime = None
        cached_value: dict = None

        @wraps(func)
        async def wrapper():
            # TODO move duplicate code to function, use transactions
            nonlocal last_accessed, cached_value

            redis = await RedisDB.create()
            now = now_func()

            if last_accessed is not None:
                # value expired and should be updated
                if last_accessed + delta < now:
                    cached_value = await func()
                    cached_value['_cache_updated'] = DatetimeDump.dump(now)
                    last_accessed = now
                    await redis.set(value_key, json.dumps(cached_value))
                    await redis.set(time_key, DatetimeDump.dump(last_accessed))

                return cached_value

            date_string = await redis.get(time_key, encoding='utf-8')

            # database does not have values
            if date_string is None:
                cached_value = await func()
                cached_value['_cache_updated'] = DatetimeDump.dump(now)
                last_accessed = now
                await redis.set(value_key, json.dumps(cached_value))
                await redis.set(time_key, DatetimeDump.dump(last_accessed))
                return cached_value

            # database have values
            last_accessed = DatetimeDump.restore(date_string)
            if last_accessed + delta < now:
                cached_value = await func()
                cached_value['_cache_updated'] = DatetimeDump.dump(now)
                last_accessed = now
                await redis.set(value_key, json.dumps(cached_value))
                await redis.set(time_key, DatetimeDump.dump(last_accessed))
                return cached_value

            cached_value = json.loads(await redis.get(value_key, encoding='utf-8'))
            return cached_value

        return wrapper

    return decorator
