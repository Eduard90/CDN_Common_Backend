from typing import Iterable

from marshmallow import fields, validate


class StringOneOf(fields.String):
    def __init__(self, values: Iterable[str], *args, **kwargs):
        all_vals = []
        for val in values:
            all_vals.append(val)
            all_vals.append(f'-{val}')
        super().__init__(*args, **kwargs, validate=validate.OneOf(all_vals))
