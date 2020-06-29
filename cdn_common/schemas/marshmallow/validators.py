from marshmallow import validate


class PageValidator(validate.Range):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, error='Wrong page')


class PageSizeValidator(validate.Range):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, error='Wrong count')
