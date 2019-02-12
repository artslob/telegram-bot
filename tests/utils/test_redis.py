import pytest

from utils.redis import RedisDB


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
