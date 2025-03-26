from typing import Dict

from litestar import get
from litestar.app import Litestar
from litestar.config.response_cache import ResponseCacheConfig
from litestar.router import Router
from litestar.stores.redis import RedisStore

from src.settings import settings


@get("/", cache=True)
async def hello_world() -> Dict[str, str]:
    return {"Hello": "World!"}


def get_app() -> Litestar:
    print(f"URL {settings.REDIS_URL}")
    redis_store = RedisStore.with_client(url=settings.REDIS_URL)
    cache_config = ResponseCacheConfig(store="redis_backed_store")

    base_route = Router("/api/v1", route_handlers=[hello_world])
    app = Litestar(
        route_handlers=[base_route],
        stores={"redis_backed_store": redis_store},
        response_cache_config=cache_config
    )
    return app
