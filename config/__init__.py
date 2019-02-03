import pathlib

# defaults
PORT = 8081
WEBHOOK_RETRIES = 5
YANDEX_API_URL = 'https://api.weather.yandex.ru/v1/forecast'

# locals
TOKEN = NotImplemented
HOST = NotImplemented
X_YANDEX_API_KEY = NotImplemented

try:
    from config.local import *
except ImportError:
    pass

PROJECT_DIR = pathlib.Path(__file__).parent.parent
LOG_BASE = PROJECT_DIR / 'logs'

API = f'https://api.telegram.org/bot{TOKEN}'


def validate_config():
    for _k, _v in tuple(globals().items()):
        if _v is NotImplemented:
            raise NotImplementedError(_k)
