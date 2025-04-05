from dishka.integrations import litestar as litestar_integration
from litestar.app import Litestar
from litestar.config.response_cache import ResponseCacheConfig
from litestar.router import Router
from litestar.stores.redis import RedisStore

from .infrastructure.di import container
from .lists_of_addictions import routes_handlers
from .logger_config import logging_config
from .modules.users.auth import oauth2
from .settings import settings


def get_app() -> Litestar:
    redis_store = RedisStore.with_client(url=settings.REDIS_URL)
    cache_config = ResponseCacheConfig(store="redis_backed_store")

    base_route = Router("/api/v1", route_handlers=routes_handlers)
    app = Litestar(
        route_handlers=[base_route],
        stores={"redis_backed_store": redis_store},
        response_cache_config=cache_config,
        middleware=[oauth2.middleware],
        debug=True,
        # on_app_init=[oauth2.on_app_init],
        logging_config=logging_config,
    )
    oauth2.on_app_init(app)
    litestar_integration.setup_dishka(container, app)
    return app
