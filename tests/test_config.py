import pytest

import config


@pytest.mark.parametrize('arg', ['TOKEN', 'HOST', 'X_YANDEX_API_KEY', 'API'])
@pytest.mark.parametrize('value', [None, '', 'test', 0, 123, {}])
def test_validate_config(arg, value, monkeypatch):
    monkeypatch.setattr(config, arg, value)
    config.validate_config()

    monkeypatch.setattr(config, arg, NotImplemented)
    with pytest.raises(NotImplementedError):
        config.validate_config()
