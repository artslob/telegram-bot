import pytest

from telegram.commands import execute_command


@pytest.mark.parametrize('txt', [None, '', 'start', 'ping', 'echo', 'test', 'some text'])
def test_no_command(txt):
    assert execute_command(txt) == 'No such command'


@pytest.mark.parametrize('txt', ['/ping', '/ping 123', '/ping\n123', '/ping\t123'])
def test_ping(txt):
    assert execute_command(txt) == 'pong!'


@pytest.mark.parametrize('txt, expected', [
    ('/echo', '/echo '),
    ('/echo text', '/echo text'),
    ('/echo     text', '/echo text'),
    ('/echo\n\ttext\ntest\t', '/echo text test'),
])
def test_echo(txt, expected):
    # TODO fix echo command
    assert execute_command(txt) == expected
