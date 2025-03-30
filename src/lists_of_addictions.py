from typing import Dict

from litestar import get

from src.modules.books.router import GenreController
from src.modules.users.router import UserController

__all__ = ["routes_handlers", "listeners"]

@get("/", cache=True)
async def hello_world() -> Dict[str, str]:
    return {"Hello": "World!"}


routes_handlers = [GenreController, UserController,hello_world]

listeners = []
