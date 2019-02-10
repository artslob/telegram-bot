import pathlib


def read_secret(name: str) -> str:
    secret = pathlib.Path(f'/run/secrets/{name}.secret')
    if not secret.is_file():
        return NotImplemented

    with open(secret) as f:
        return f.readline().strip()


# defaults
PORT = 8081
WEBHOOK_RETRIES = 5
YANDEX_API_URL = 'https://api.weather.yandex.ru/v1/forecast'

# secrets
TOKEN = read_secret('token')
HOST = read_secret('host')
X_YANDEX_API_KEY = read_secret('x_yandex_api_key')

PROJECT_DIR = pathlib.Path(__file__).parent.parent
LOG_BASE = PROJECT_DIR / 'logs'

API = f'https://api.telegram.org/bot{TOKEN}'


def validate_config():
    for _k, _v in tuple(globals().items()):
        if _v is NotImplemented:
            raise NotImplementedError(_k)
