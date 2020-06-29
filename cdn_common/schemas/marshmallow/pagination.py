from marshmallow import Schema, fields, EXCLUDE

from common.schemas.marshmallow.validators import PageValidator, PageSizeValidator


class SmallPaginationSchema(Schema):
    max_page_size = 100
    page = fields.Integer(default=1, validate=PageValidator(1))
    page_size = fields.Integer(default=10, validate=PageSizeValidator(1, max_page_size))

    class Meta:
        unknown = EXCLUDE


class LargePaginationSchema(Schema):
    max_page_size = 1000
    page = fields.Integer(default=1, validate=PageValidator(1))
    page_size = fields.Integer(default=50, validate=PageSizeValidator(1, max_page_size))

    class Meta:
        unknown = EXCLUDE
