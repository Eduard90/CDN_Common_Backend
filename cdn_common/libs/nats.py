import functools

from google.protobuf.json_format import MessageToDict


def nats_debug(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        msg = args[0]
        logger = kwargs.get('app').nats_logger
        logger.debug(f'Message: {msg}')
        res = await func(*args, **kwargs)
        return res
    return inner


def nats_parse(pb_schema, mm_schema=None):
    """Parse message through Protobuf schema and Marshmallow"""
    def decorator_nats_parse(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            msg = args[0]

            logger = kwargs.get('app').nats_logger
            logger.debug(f'PBSchema: "{pb_schema}", MMSchema: "{mm_schema}", Message: {msg}')

            try:
                schema_inst = pb_schema()
                schema_inst.ParseFromString(msg.data)
                logger.debug(f'[APP] Message: {MessageToDict(schema_inst)}')
                kwargs['data'] = schema_inst
            except Exception as e:
                # TODO: Reraise exception with detail error
                print('error', e, type(e))
                return

            res = await func(*args, **kwargs)
            return res
        return inner
    return decorator_nats_parse
