import argparse

import config


def positive_int(arg):
    try:
        arg = int(arg)
    except (ValueError, TypeError):
        raise argparse.ArgumentTypeError(f'not integer value: {arg!r}')
    if arg <= 0:
        raise argparse.ArgumentTypeError('value should be positive')

    return arg


def get_parser():
    parser = argparse.ArgumentParser(description='Arguments for bot.')
    parser.add_argument('-p', '--port', dest='port', type=positive_int, default=config.PORT,
                        help='Port on which webhook is registered on. Default is provided by config file: %(default)s.')
    return parser
