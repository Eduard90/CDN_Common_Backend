import os

from yarl import URL


def getenv_boolean(name: str, default: bool = False) -> bool:
    value = os.getenv(name, default)
    if isinstance(value, str):
        return value.lower() == 'true'
    return value


def getenv_string(name: str, default: str = '') -> str:
    value = os.getenv(name)
    if value is None or value == '':
        return default
    return value


def getenv_integer(name: str, default: int = 0) -> int:
    return int(getenv_string(name, str(default)))


def secure_connect_string(connect_string: str) -> str:
    connect_url = URL(connect_string)
    secure_password = None
    if connect_url.password:
        secure_password = hide_password(connect_url.password)
    return str(connect_url.with_password(secure_password))


def hide_password(password: str) -> str:
    if len(password) <= 3:
        return '*' * 3

    return f'{password[0]}***{password[-1]}'


