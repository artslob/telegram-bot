import warnings
from abc import ABCMeta, abstractmethod

from api.weather.yandex import YandexWeather, BaseError as YandexWeatherBaseError
from telegram.objects import Update

commands = {}


class CommandMetaclass(ABCMeta):
    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        command = dct.get('_command')
        if command:
            if command in commands:
                warnings.warn(f'command {command!r} already in methods')
            commands[cls.command()] = cls
        return cls


class AbstractCommand(metaclass=CommandMetaclass):
    _command = ''

    def __init__(self, update: Update, params: list):
        self.update = update
        self.params = params

    @classmethod
    def command(cls) -> str:
        return f'/{cls._command}'

    @classmethod
    def description(cls):
        return cls.__doc__

    @abstractmethod
    async def result(self) -> str:
        pass


class StartCommand(AbstractCommand):
    """print available commands"""

    _command = 'start'

    async def result(self) -> str:
        command_list = '\n'.join(f'{cmd} - {cls.description()}' for cmd, cls in commands.items())
        return f'Hello! I can process such commands:\n{command_list}'


class EchoCommand(AbstractCommand):
    """print input string"""

    _command = 'echo'

    async def result(self) -> str:
        return f'{self.command()} {" ".join(self.params)}'


class PingPongCommand(AbstractCommand):
    """check bot availability"""

    _command = 'ping'

    async def result(self) -> str:
        return 'pong!'


class WeatherCommand(AbstractCommand):
    """returns current weather in SPb"""

    _command = 'weather'

    async def result(self) -> str:
        try:
            return await YandexWeather.weather_description()
        except YandexWeatherBaseError as e:
            return f'Sorry. Error occurred during the request to API.\n{e}'
        except KeyError:
            return f'Sorry. Something went wrong while parsing answer from API.'


async def execute_command(update: Update):
    no_command = 'No such command'
    text = update.message.text

    if not text:
        return no_command

    command, *params = text.split()
    cls = commands.get(command)
    if not cls:
        return no_command

    return await cls(update, params).result()


if __name__ == '__main__':
    for _cls in commands.values():
        print(f'{_cls._command} - {_cls.description()}')
