import functools
from nats.aio.client import Client as NATS


def init_nats(max_reconnect: int):
    async def inner(app):
        async def on_error(e):
            app.nats_logger.error(f'[NATS] Error: {e}')

        async def on_close():
            app.nats_logger.warning('[NATS] Closed connection to NATS')

        async def on_reconnect():
            app.nats_logger.warning(f'[NATS] Reconnected to NATS: {app.nats_dsn}')

        async def on_disconnect():
            app.nats_logger.warning('[NATS] Disconnected from NATS')

        app.nats_logger.info(f'[NATS] Connecting to NATS: {app.nats_dsn} ...')
        nc = NATS()

        await nc.connect(app.nats_dsn, error_cb=on_error, closed_cb=on_close, reconnected_cb=on_reconnect,
                         disconnected_cb=on_disconnect, max_reconnect_attempts=max_reconnect)
        app['nats'] = nc
        app.nats_logger.info('[NATS] Connected to NATS!')
    return inner


async def close_nats(app):
    if app['nats'].is_connected:
        app.nats_logger.debug('Close NATS connection...')
        await app['nats'].close()
        app.nats_logger.debug('Closed NATS connection!')


def init_handlers(handlers: dict):
    async def inner(app):
        """Subscribe and set callbacks"""
        hndls_dict = handlers

        for subject, hndls in hndls_dict.items():
            hndls_names = []
            if not isinstance(hndls, list):
                hndls = [hndls]

            for hndl_raw in hndls:
                hndl = functools.partial(hndl_raw, app=app)
                await app['nats'].subscribe(subject, cb=hndl)
                hndls_names.append(f'{hndl_raw.__module__}.{hndl_raw.__name__}')

            app.nats_logger.info(f'[NATS] Subscribed to "{subject}", handlers: {hndls_names}')
    return inner
