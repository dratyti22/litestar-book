from litestar.connection import ASGIConnection
from litestar.security.jwt.auth import OAuth2PasswordBearerAuth
from litestar.security.jwt.token import Token
from sqlalchemy import select

from src.modules.users.model import UserDb
from src.settings import settings


async def retrieve_user_handler(
    token: Token,
    connection: ASGIConnection
) -> UserDb | None:
    session = connection.app.state.session
    result = await session.execute(select(UserDb).where(UserDb.id == int(token.sub)))
    return result.scalar_one_or_none()


o2auth = OAuth2PasswordBearerAuth[UserDb](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.JWT_SECRET,
    token_url="/api/v1/user/login",
    exclude=["/api/v1/user/login", "/api/v1/user/register", "/schema"]
)
