from typing import Dict

from litestar import get, Router

from src.modules.books.router import GenreController, BookController
from src.modules.users.router import UserController

__all__ = ["base_route", "listeners"]


@get("/", cache=True)
async def hello_world() -> Dict[str, str]:
    return {"Hello": "World!"}


routes_handlers = [GenreController, BookController, UserController, hello_world]
base_route = Router("/api/v1", route_handlers=routes_handlers)

listeners = []
