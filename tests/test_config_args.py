import pytest

from config.args import get_parser


@pytest.fixture
def parse():
    def _parse(args):
        return get_parser().parse_args(args)

    return _parse


@pytest.mark.parametrize('number', ['8081', '80'])
def test_port(parse, number):
    assert parse(['-p', number]).port == int(number)


@pytest.mark.parametrize('number', ['-80', '0'])
def test_port_not_positive(parse, capsys, number):
    with pytest.raises(SystemExit):
        parse(['-p', number])
    captured = capsys.readouterr()
    assert captured.err.endswith('error: argument -p/--port: value should be positive\n')


@pytest.mark.parametrize('number', ['asd', '1a3', '0x30'])
def test_port_not_integer(parse, capsys, number):
    with pytest.raises(SystemExit):
        parse(['-p', number])
    captured = capsys.readouterr()
    assert captured.err.endswith(f"error: argument -p/--port: not integer value: '{number}'\n")
