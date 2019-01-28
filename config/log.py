from logging.config import dictConfig

from config import LOG_BASE

LOGGING = {
    'version': 1,
    'root': {
        'level': 'DEBUG',
        'handlers': ['root'],
    },
    'loggers': {
        'webhook': {
            'level': 'DEBUG',
            'handlers': ['webhook', 'errors', 'console'],
            'propagate': False,
        },
    },
    'handlers': {
        'root': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'defaultFormatter',
            'filename': str(LOG_BASE / 'root.log'),
        },
        'webhook': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'defaultFormatter',
            'filename': str(LOG_BASE / 'webhook.log'),
        },
        'errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            # TODO add module and line fields to errors formatter
            'formatter': 'defaultFormatter',
            'filename': str(LOG_BASE / 'errors.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'defaultFormatter',
        },
    },
    'formatters': {
        'defaultFormatter': {
            'class': 'logging.Formatter',
            'format': '[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%d %b %Y %H:%M:%S',
        },
    },
}


def init_log():
    dictConfig(LOGGING)
