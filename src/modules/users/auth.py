from litestar.connection import ASGIConnection
from litestar.security.jwt.auth import OAuth2PasswordBearerAuth
from litestar.security.jwt.token import Token

from src.infrastructure.di import container
from src.infrastructure.provide import AuthService
from src.modules.users.model import UserDb
from src.settings import settings


async def retrieve_user_handler(
    token: Token,
    connection: ASGIConnection,
) -> UserDb | None:
    try:
        connection.logger.debug(f"Received token: {token.__dict__}")
        print("=== CALLED retrieve_user_handler ===")
        if not token.sub:
            connection.logger.error("Token 'sub' is missing")
            return None

        try:
            user_id = int(token.sub)
        except ValueError:
            connection.logger.error(f"Invalid user ID in token: {token.sub}")
            return None

        connection.logger.debug(f"Searching for user ID: {user_id}")
        async with container() as scope:
            auth_service =await scope.get(AuthService)
            user = await auth_service.get_user_by_id(user_id)

        if not user:
            connection.logger.error(f"User {user_id} not found")

        return user

    except Exception as e:
        connection.logger.exception(f"Critical error in auth handler: {e}")
        return None


oauth2 = OAuth2PasswordBearerAuth[UserDb](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=settings.JWT_SECRET,
    token_url="/api/v1/user/login",
    exclude=["/api/v1/user/login", "/api/v1/user/register", "/schema"]
)
