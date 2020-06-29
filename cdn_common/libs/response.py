import json
from functools import partial
from typing import Union

from aiohttp import web


ctype = 'application/json'
dumps_func = partial(json.dumps, ensure_ascii=False)


class ErrorResponse:
    __code: int
    __errors: dict
    __message: str

    def __init__(self, code: int, errors: dict, message: str = ''):
        super().__init__()
        self.__code = code
        self.__errors = errors
        self.__message = message

    def to_dict(self) -> dict:
        return dict(code=self.__code, errors=self.__errors, message=self.__message)


def paginated_response(count: int, max_page_size: int, results: list) -> web.Response:
    resp_data = {
        'pagination': {'total_count': count, 'on_page': len(results), 'max_page_size': max_page_size},
        'results': results
    }
    return json_response(resp_data)


def json_response(data: Union[list, dict]) -> web.Response:
    return web.json_response(data, dumps=dumps_func)


def HTTPNotFound(data: dict):
    return web.HTTPNotFound(text=dumps_func(data), content_type=ctype)


def HTTPBadRequest(data: dict):
    return web.HTTPBadRequest(text=dumps_func(data), content_type=ctype)
