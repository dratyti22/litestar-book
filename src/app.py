from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar.app import Litestar
from litestar.config.response_cache import ResponseCacheConfig
from litestar.router import Router
from litestar.stores.redis import RedisStore

from .infrastructure.provide import AppProvider
from .settings import settings, Settings
from .lists_of_addictions import routes_handlers

container = make_async_container(AppProvider(), context={Settings: settings})

def get_app() -> Litestar:
    redis_store = RedisStore.with_client(url=settings.REDIS_URL)
    cache_config = ResponseCacheConfig(store="redis_backed_store")

    base_route = Router("/api/v1", route_handlers=routes_handlers)
    app = Litestar(
        route_handlers=[base_route],
        stores={"redis_backed_store": redis_store},
        response_cache_config=cache_config
    )
    litestar_integration.setup_dishka(container, app)
    return app
