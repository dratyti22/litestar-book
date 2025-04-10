from dishka.integrations import litestar as litestar_integration
from litestar.app import Litestar
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.config.response_cache import ResponseCacheConfig
from litestar.stores.redis import RedisStore

from .infrastructure.di import container
from .infrastructure.middleware import CheckUserActivateMiddleware
from .lists_of_addictions import base_route
from .logger_config import logging_config
from .modules.users.auth import oauth2
from .settings import settings


def get_app() -> Litestar:
    redis_store = RedisStore.with_client(url=settings.REDIS_URL)
    cache_config = ResponseCacheConfig(store="redis_backed_store")

    cors_config = CORSConfig(
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )
    csrf_config = CSRFConfig(
        secret=settings.CSRF_SECRET,
        safe_methods={"GET", "HEAD", "OPTIONS"}
    )

    app = Litestar(
        route_handlers=[base_route],
        stores={"redis_backed_store": redis_store},
        response_cache_config=cache_config,
        debug=True,
        middleware=[oauth2.middleware, CheckUserActivateMiddleware()],
        logging_config=logging_config,
        cors_config=cors_config,
        csrf_config=csrf_config,
    )
    oauth2.on_app_init(app)
    litestar_integration.setup_dishka(container, app)
    return app
