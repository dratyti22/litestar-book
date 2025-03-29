from typing import Dict

from litestar import get

from src.modules.books.router import GenreController


@get("/", cache=True)
async def hello_world() -> Dict[str, str]:
    return {"Hello": "World!"}


routes_handlers = [GenreController, hello_world]

listeners = []
