from abc import ABC, abstractmethod


# TODO value can be list

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
