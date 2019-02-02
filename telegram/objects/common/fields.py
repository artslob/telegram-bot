from typing import TypeVar

# TODO value can be list

T = TypeVar('T')


def telegram_field(factory: T, value, *, required=False) -> T:
    base = True if issubclass(factory, (int, str, bool, float)) else False
    if value is None and not required:
        return None
    if value is None and required:
        raise ValueError('required value is None')

    if base:
        return factory(value)

    return factory.from_dict(value)
