from aiohttp import web
from loguru import logger
import ujson
from api.constants import settings, URL
from api.utilities import check_if_phone_number_exist_in_stop_list, PhoneNumberValidationError, apply_migrations
from database import db


async def check_phone_number(request: web.Request) -> web.Response:
    """Check if phone number is in the block list"""
    try:
        phone_number = request.match_info['phone_number']
        result = await check_if_phone_number_exist_in_stop_list(phone_number)
        logger.info(f'Successful attempt to check the phone number with result:{result}')
        return web.json_response({'found': result}, dumps=ujson.dumps)
    except PhoneNumberValidationError as error:
        logger.info('Getting invalid phone number to check')
        return web.json_response({'error': str(error)}, dumps=ujson.dumps)


async def create_app() -> web.Application:
    """Create web application"""
    logger.debug('Starting up web app')
    app = web.Application(debug=settings.debug)
    app.add_routes(
        [
            web.get('/check_phone_number/{phone_number}', check_phone_number),
        ]
    )
    app.on_cleanup.append(on_cleanup)
    await db.set_bind(URL.DB_URL_INSIDE_CONTAINER.value)
    apply_migrations()
    logger.debug('Finished starting process')
    return app


async def on_cleanup(app: web.Application) -> None:
    """Closing connection to db"""
    logger.debug('Closing db connection')
    await db.pop_bind().close()
    logger.debug('Shutting down web app')
