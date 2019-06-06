from typing import TypeVar

# TODO value can be list

T = TypeVar('T')


def telegram_field(factory: T, value, *, required=False) -> T:
    if value is None and not required:
        return None
    if value is None and required:
        raise ValueError('required value is None')

    if issubclass(factory, (int, str, bool, float)):
        return factory(value)

    return factory.from_dict(value)
