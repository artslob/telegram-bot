import pathlib

from config.defaults import *
from config.local import *

PROJECT_DIR = pathlib.Path(__file__).parent.parent
LOG_BASE = PROJECT_DIR / 'logs'

API = f'https://api.telegram.org/bot{TOKEN}'


for _k, _v in tuple(globals().items()):
    if _v is NotImplemented:
        raise NotImplementedError(_k)
