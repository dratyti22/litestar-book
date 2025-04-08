from litestar.middleware import ASGIMiddleware
from litestar.types import Scope, Receive, Send, ASGIApp
from litestar.exceptions import HTTPException

from src.modules.users.auth import oauth2


class CheckUserActivateMiddleware(ASGIMiddleware):
    async def handle(self, scope: Scope, receive: Receive, send: Send, next_app: ASGIApp) -> None:
        route_handler = scope.get('route_handler')
        path = scope.get('path', '')

        if not route_handler or path in oauth2.exclude:
            await next_app(scope, receive, send)

        if getattr(route_handler, "exclude_from_auth", False):
            await next_app(scope, receive, send)

        user = scope.get("user")
        if user and not user.is_activate:
            raise HTTPException(status_code=403, detail="User is not is_activate")

        await next_app(scope, receive, send)
