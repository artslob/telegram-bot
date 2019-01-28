import aiohttp

import config
from api.weather.yandex.exceptions import ForbiddenRequestError, UnknownRequestError


class YandexWeather:
    prec_type = {
        0: 'no precipitation',
        1: 'rain',
        2: 'rain with snow',
        3: 'snow',
    }

    prec_strength = {
        0: 'no precipitation',
        0.25: 'weak rain/snow',
        0.5: 'rain/snow',
        0.75: 'strong rain/snow',
        1: 'very strong rain/snow',
    }

    cloudiness = {
        0: 'clear',
        0.25: 'overcast',
        0.5: 'cloudy with clear spells',
        0.75: 'cloudy with clear spells',
        1: 'mainly cloudy',
    }

    @classmethod
    async def get_weather(cls) -> dict:
        headers = {'X-Yandex-API-Key': config.X_YANDEX_API_KEY}

        params = {
            'lat': '59.93863', 'lon': '30.31413',
            'lang': 'ru_RU',
            'limit': '1',
            'hours': 'false',
            'extra': 'true',
        }

        kwargs = dict(url=config.YANDEX_API_URL, params=params, headers=headers)

        async with aiohttp.request('GET', **kwargs) as response:
            if response.status == 403:
                raise ForbiddenRequestError()
            elif response.status != 200:
                raise UnknownRequestError()

            return await response.json()

    @classmethod
    def stringify(cls, dct: dict) -> str:
        # TODO forecasts
        result = [
            f'Detailed: {dct["info"]["url"]}',
            f'Temperature: {dct["fact"]["temp"]} °C',
            f'Condition: {dct["fact"]["condition"]}',
            f'Wind speed: {dct["fact"]["wind_speed"]} m/s',
            f'Humidity: {dct["fact"]["humidity"]} %',
        ]

        if 'prec_type' in dct['fact']:
            result.append(f'Precipitation: {cls.prec_type.get(dct["fact"]["prec_type"], "unknown")}')

        if 'prec_strength' in dct['fact']:
            result.append(f'Precipitation strength: {cls.prec_strength.get(dct["fact"]["prec_strength"], "unknown")}')

        if 'cloudness' in dct['fact']:
            result.append(f'Cloudiness: {cls.cloudiness.get(dct["fact"]["cloudness"], "unknown")}')

        result.append('According to Yandex.Weather')

        return '\n'.join(result)
