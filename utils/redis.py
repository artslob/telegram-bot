import aioredis

import config


class RedisDB:
    _redis: aioredis.Redis = None

    @classmethod
    async def create(cls):
        if cls._redis is not None:
            return cls._redis

        cls._redis = await aioredis.create_redis_pool(f'redis://{config.REDIS_HOST}')
        return cls._redis
