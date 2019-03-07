import pytest

from telegram.objects import Update
from telegram.objects.common.base import TelegramObject
from utils.redis import RedisDB


@pytest.fixture()
def dict_parser():
    def parser(factory: TelegramObject):
        def from_dict(dct: dict):
            return factory.from_dict(dct)

        return from_dict

    return parser


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


@pytest.fixture
def update_dict():
    def dict_factory(text):
        return {
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
            }
        }

    return dict_factory


@pytest.fixture
def update_object(update_dict):
    def get_object(text):
        return Update.from_dict(update_dict(text))

    return get_object


@pytest.fixture
def async_context_response():
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


@pytest.fixture
def yandex_weather_json():
    return {
        "now": 1548691222,
        "now_dt": "2019-01-28T16:00:22.587Z",
        "info": {
            "f": True,
            "n": True,
            "nr": True,
            "ns": True,
            "nsr": True,
            "p": True,
            "lat": 59.93863,
            "lon": 30.31413,
            "tzinfo": {
                "name": "Europe/Moscow",
                "abbr": "MSK",
                "offset": 10800,
                "dst": False
            },
            "def_pressure_mm": 759,
            "def_pressure_pa": 1012,
            "_h": False,
            "url": "https://yandex.ru/pogoda/?lat=59.93863&lon=30.31413"
        },
        "fact": {
            "temp": -14,
            "feels_like": -19,
            "temp_water": 0,
            "icon": "bkn_n",
            "condition": "cloudy",
            "wind_speed": 2,
            "wind_gust": 8.2,
            "wind_dir": "e",
            "pressure_mm": 756,
            "pressure_pa": 1008,
            "humidity": 78,
            "uv_index": 0,
            "soil_temp": -2,
            "soil_moisture": 0.21,
            "daytime": "n",
            "polar": False,
            "season": "winter",
            "obs_time": 1548690425,
            "accum_prec": {
                "1": 0,
                "3": 3,
                "7": 3.9
            },
            "source": "station"
        },
        "forecasts": [
            {
                "date": "2019-01-28",
                "date_ts": 1548622800,
                "week": 5,
                "sunrise": "09:22",
                "sunset": "17:01",
                "rise_begin": "08:33",
                "set_end": "17:50",
                "moon_code": 4,
                "moon_text": "last-quarter",
                "parts": {
                    "night": {
                        "_source": "0,1,2,3,4,5",
                        "temp_min": -21,
                        "temp_max": -18,
                        "temp_avg": -19,
                        "feels_like": -23,
                        "temp_water": 0,
                        "icon": "bkn_-sn_n",
                        "condition": "overcast-and-light-snow",
                        "daytime": "n",
                        "polar": False,
                        "wind_speed": 1.2,
                        "wind_gust": 3.2,
                        "wind_dir": "se",
                        "pressure_mm": 756,
                        "pressure_pa": 1008,
                        "humidity": 81,
                        "uv_index": 0,
                        "soil_temp": -1,
                        "soil_moisture": 0.21,
                        "prec_mm": 0.6,
                        "prec_period": 360,
                        "prec_prob": 80
                    },
                    "morning": {
                        "_source": "6,7,8,9,10,11",
                        "temp_min": -20,
                        "temp_max": -17,
                        "temp_avg": -18,
                        "feels_like": -23,
                        "temp_water": 0,
                        "icon": "bkn_-sn_n",
                        "condition": "overcast-and-light-snow",
                        "daytime": "n",
                        "polar": False,
                        "wind_speed": 2.5,
                        "wind_gust": 5.2,
                        "wind_dir": "e",
                        "pressure_mm": 758,
                        "pressure_pa": 1011,
                        "humidity": 81,
                        "uv_index": 0,
                        "soil_temp": -1,
                        "soil_moisture": 0.21,
                        "prec_mm": 0.6,
                        "prec_period": 360,
                        "prec_prob": 70
                    },
                    "day": {
                        "_source": "12,13,14,15,16,17",
                        "temp_min": -16,
                        "temp_max": -13,
                        "temp_avg": -14,
                        "feels_like": -20,
                        "temp_water": 0,
                        "icon": "bkn_-sn_d",
                        "condition": "overcast-and-light-snow",
                        "daytime": "d",
                        "polar": False,
                        "wind_speed": 3.3,
                        "wind_gust": 7,
                        "wind_dir": "e",
                        "pressure_mm": 757,
                        "pressure_pa": 1010,
                        "humidity": 82,
                        "uv_index": 0,
                        "soil_temp": -2,
                        "soil_moisture": 0.21,
                        "prec_mm": 0.3,
                        "prec_period": 360,
                        "prec_prob": 70
                    },
                    "evening": {
                        "_source": "18,19,20,21,22,23",
                        "temp_min": -14,
                        "temp_max": -11,
                        "temp_avg": -12,
                        "feels_like": -18,
                        "temp_water": 0,
                        "icon": "bkn_-sn_n",
                        "condition": "overcast-and-light-snow",
                        "daytime": "n",
                        "polar": False,
                        "wind_speed": 4.1,
                        "wind_gust": 8.5,
                        "wind_dir": "e",
                        "pressure_mm": 756,
                        "pressure_pa": 1008,
                        "humidity": 84,
                        "uv_index": 0,
                        "soil_temp": -2,
                        "soil_moisture": 0.21,
                        "prec_mm": 0.3,
                        "prec_period": 360,
                        "prec_prob": 80
                    },
                    "day_short": {
                        "_source": "8,9,10,11,12,13,14,15,16,17,18,19,20",
                        "temp": -13,
                        "temp_min": -20,
                        "feels_like": -19,
                        "temp_water": 0,
                        "icon": "bkn_-sn_d",
                        "condition": "overcast-and-light-snow",
                        "wind_speed": 4,
                        "wind_gust": 8.2,
                        "wind_dir": "e",
                        "pressure_mm": 757,
                        "pressure_pa": 1010,
                        "humidity": 82,
                        "uv_index": 0,
                        "soil_temp": -2,
                        "soil_moisture": 0.21,
                        "prec_mm": 0.7,
                        "prec_prob": 70
                    },
                    "night_short": {
                        "temp": -21,
                        "feels_like": -26,
                        "temp_water": 0,
                        "icon": "bkn_-sn_n",
                        "condition": "overcast-and-light-snow",
                        "wind_speed": 1.2,
                        "wind_gust": 3.2,
                        "wind_dir": "se",
                        "pressure_mm": 756,
                        "pressure_pa": 1008,
                        "humidity": 81,
                        "uv_index": 0,
                        "soil_temp": -1,
                        "soil_moisture": 0.21,
                        "prec_mm": 0.6,
                        "prec_prob": 80
                    }
                }
            },
        ]
    }
