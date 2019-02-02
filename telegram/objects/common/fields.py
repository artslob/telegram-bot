from abc import ABC, abstractmethod
from typing import TypeVar

# TODO value can be list

# TODO make fields static factories, without need to create instance at class level of telegram object (move to init)

T = TypeVar('T')


def telegram_field(factory: T, value, *, required=False) -> T:
    base = True if issubclass(factory, (int, str, bool, float)) else False
    if value is None and not required:
        return None
    if value is None and required:
        raise ValueError('required value is None')

    if base:
        return factory(value)

    return factory.from_dict(value)


class TelegramField(ABC):
    def __init__(self, factory):
        self.factory = factory
        self.base = True if issubclass(factory, (int, str, bool, float)) else False

    @abstractmethod
    def should_return_empty(self, value):
        pass

    def __call__(self, value):
        if self.should_return_empty(value):
            return None
        if self.base:
            return self.factory(value)
        return self.factory.from_dict(value)


class RequiredField(TelegramField):
    def should_return_empty(self, value):
        return False


class OptionalField(TelegramField):
    def should_return_empty(self, value):
        if value is None:
            return True
