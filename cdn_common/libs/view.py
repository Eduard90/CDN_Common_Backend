import functools

from common.libs.response import HTTPBadRequest
from common.schemas.marshmallow.pagination import SmallPaginationSchema, LargePaginationSchema


class Paginator:
    def __init__(self, page: int, page_size: int, max_page_size: int):
        super().__init__()
        self.__page = page
        self.__page_size = page_size
        self.__max_page_size = max_page_size

    @property
    def page(self) -> int:
        return self.__page

    @property
    def page_size(self) -> int:
        return self.__page_size

    @property
    def max_page_size(self) -> int:
        return self.__max_page_size


def paginated_view(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        request = args[0]
        schema = SmallPaginationSchema()
        valid = schema.validate(request.query)
        if valid:
            raise HTTPBadRequest({'code': -1000, 'errors': valid})

        page_data = schema.dump(request.query)
        paginator = Paginator(**page_data, max_page_size=schema.max_page_size)
        kwargs['paginator'] = paginator
        return await func(*args, **kwargs)

    return inner


def large_paginated_view(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        request = args[0]
        schema = LargePaginationSchema()
        valid = schema.validate(request.query)
        if valid:
            raise HTTPBadRequest({'code': -1000, 'errors': valid})

        page_data = schema.dump(request.query)
        paginator = Paginator(**page_data, max_page_size=schema.max_page_size)
        kwargs['paginator'] = paginator
        return await func(*args, **kwargs)

    return inner


