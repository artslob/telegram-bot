import logging
import warnings
from abc import ABCMeta, abstractmethod

from api.weather.yandex import YandexWeather, BaseError as YandexWeatherBaseError
from telegram.objects import Update, SendMessageObject

commands = {}

error_log = logging.getLogger('errors')


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

    def __init__(self, chat_id, update: Update, params: list):
        self.chat_id = chat_id
        self.update = update
        self.params = params

    @classmethod
    def command(cls) -> str:
        return f'/{cls._command}'

    @classmethod
    def description(cls):
        return cls.__doc__

    @abstractmethod
    async def result(self) -> SendMessageObject:
        pass


class StartCommand(AbstractCommand):
    """print available commands"""

    _command = 'start'

    async def result(self) -> SendMessageObject:
        command_list = '\n'.join(f'{cmd} - {cls.description()}' for cmd, cls in commands.items())
        text = f'Hello! I can process such commands:\n{command_list}'
        return SendMessageObject(self.chat_id, text)


class EchoCommand(AbstractCommand):
    """print input telegram Update object"""

    _command = 'echo'

    async def result(self) -> SendMessageObject:
        text = f'```\n{self.update.to_str()}\n```'
        return SendMessageObject(self.chat_id, text, parse_mode='markdown')


class PingPongCommand(AbstractCommand):
    """check bot availability"""

    _command = 'ping'

    async def result(self) -> SendMessageObject:
        return SendMessageObject(self.chat_id, 'pong!')


class WeatherCommand(AbstractCommand):
    """returns current weather in SPb"""

    _command = 'weather'

    async def result(self) -> SendMessageObject:
        try:
            text = await YandexWeather.weather_description()
        except YandexWeatherBaseError as e:
            error_log.exception('API error')
            text = f'Sorry. Error occurred during the request to API.\n{e}'
        except KeyError:
            error_log.exception('parsing error')
            text = f'Sorry. Something went wrong while parsing answer from API.'
        return SendMessageObject(self.chat_id, text)


async def execute_command(chat_id, update: Update) -> SendMessageObject:
    no_command = SendMessageObject(chat_id, 'No such command')
    text = update.message.text

    if not text:
        return no_command

    command, *params = text.split()
    cls = commands.get(command)
    if not cls:
        return no_command

    return await cls(chat_id, update, params).result()


if __name__ == '__main__':
    for _cls in commands.values():
        print(f'{_cls._command} - {_cls.description()}')
