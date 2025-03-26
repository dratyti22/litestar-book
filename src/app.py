from typing import Dict

from dishka import make_async_container
from litestar import get
from litestar.app import Litestar
from litestar.config.response_cache import ResponseCacheConfig
from litestar.router import Router
from litestar.stores.redis import RedisStore

from src.infrastructure.provide import AppProvider
from src.settings import settings, Settings
from dishka.integrations import litestar as litestar_integration

container = make_async_container(AppProvider(), context={Settings: settings})


@get("/", cache=True)
async def hello_world() -> Dict[str, str]:
    return {"Hello": "World!"}


def get_app() -> Litestar:
    redis_store = RedisStore.with_client(url=settings.REDIS_URL)
    cache_config = ResponseCacheConfig(store="redis_backed_store")

    base_route = Router("/api/v1", route_handlers=[hello_world])
    app = Litestar(
        route_handlers=[base_route],
        stores={"redis_backed_store": redis_store},
        response_cache_config=cache_config
    )
    litestar_integration.setup_dishka(container, app)
    return app
