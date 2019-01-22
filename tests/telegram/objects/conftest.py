import pytest

from telegram.objects.common.base import TelegramObject


@pytest.fixture()
def dict_parser():
    def parser(factory: TelegramObject):
        def from_dict(dct: dict):
            return factory.from_dict(dct)

        return from_dict

    return parser
