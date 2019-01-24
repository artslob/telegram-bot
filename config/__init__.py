import pathlib

# defaults
PORT = 8081
WEBHOOK_RETRIES = 5

# locals
TOKEN = NotImplemented
HOST = NotImplemented

from config.local import *

PROJECT_DIR = pathlib.Path(__file__).parent.parent
LOG_BASE = PROJECT_DIR / 'logs'

API = f'https://api.telegram.org/bot{TOKEN}'


def validate_config():
    for _k, _v in tuple(globals().items()):
        if _v is NotImplemented:
            raise NotImplementedError(_k)
