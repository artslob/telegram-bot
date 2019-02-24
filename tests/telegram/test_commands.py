import pytest

from telegram.commands import execute_command


@pytest.mark.parametrize('txt', [None, '', 'start', 'ping', 'echo', 'test', 'some text'])
async def test_no_command(update_object, txt):
    assert await execute_command(update_object(txt)) == 'No such command'


@pytest.mark.parametrize('txt', ['/ping', '/ping 123', '/ping\n123', '/ping\t123'])
async def test_ping(update_object, txt):
    assert await execute_command(update_object(txt)) == 'pong!'


@pytest.mark.parametrize('txt', ['/echo', '/echo text', '/echo     text', '/echo\n\ttext\ntest\t'])
async def test_echo(update_object, txt):
    assert await execute_command(update_object(txt)) == update_object(txt).to_str()
