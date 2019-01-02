import warnings
from abc import ABCMeta, abstractmethod

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

    def __init__(self, *params):
        self.params = params

    @classmethod
    def command(cls) -> str:
        return f'/{cls._command}'

    @classmethod
    def description(cls):
        return cls.__doc__

    @abstractmethod
    def result(self) -> str:
        pass


class StartCommand(AbstractCommand):
    """print available commands"""

    _command = 'start'

    def result(self) -> str:
        command_list = '\n'.join(f'{cmd} - {cls.description()}' for cmd, cls in commands.items())
        return f'Hello! I can process such commands:\n{command_list}'


class EchoCommand(AbstractCommand):
    """print input string"""

    _command = 'echo'

    def result(self) -> str:
        return f'{self.command()} {" ".join(self.params)}'


def execute_command(text: str):
    command, *params = text.split()
    cls = commands.get(command)
    if not cls:
        return 'No such command'
    obj = cls(*params)
    return obj.result()


if __name__ == '__main__':
    for _cmd, _cls in commands.items():
        print(f'{_cmd} - {_cls.description()}')
