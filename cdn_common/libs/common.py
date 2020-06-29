from yarl import URL


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
