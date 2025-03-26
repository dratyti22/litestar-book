from typing import Dict

from litestar import get
from litestar.app import Litestar
from litestar.router import Router


@get("/{name:str}")
async def hello_world(name: str) -> Dict[str, str]:
    return {"Hello": name}


def get_app() -> Litestar:
    base_route = Router("/api/v1", route_handlers=[hello_world])
    app = Litestar(route_handlers=[base_route])
    return app
