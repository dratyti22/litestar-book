from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers import BaseRouteHandler


async def admin_user_guard(connection: ASGIConnection, _: BaseRouteHandler):
    if not await connection.user.is_admin:
        raise NotAuthorizedException()
