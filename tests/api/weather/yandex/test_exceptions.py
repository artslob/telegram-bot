import pytest

from api.weather.yandex import BaseError, RequestError, ForbiddenRequestError, UnknownRequestError


@pytest.mark.parametrize('error_type', [BaseError, RequestError, ForbiddenRequestError, UnknownRequestError])
@pytest.mark.parametrize('arg', [None, 'some error message', 123, ['some', 'list']])
def test_base_exception(error_type, arg):
    with pytest.raises(error_type) as exc_info:
        raise error_type(arg)

    if arg is None:
        assert str(exc_info.value) == error_type.__doc__
    else:
        assert str(exc_info.value) == str(arg)
