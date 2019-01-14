from config.defaults import *
from config.local import *

API = f'https://api.telegram.org/bot{TOKEN}'


for _k, _v in tuple(globals().items()):
    if _v is NotImplemented:
        raise NotImplementedError(_k)
