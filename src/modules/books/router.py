from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import post, HttpMethod, route
from litestar.controller import Controller

from src.modules.books.protocols import GenreProtocol
from src.modules.books.schema import GenresDTO, WriteGenreDTO


class GenreController(Controller):
    path = "/genre"

    @route(http_method=HttpMethod.GET, path="/", exclude_from_auth=True, cached=3600)
    @inject
    async def get_all_genres(self, service: FromDishka[GenreProtocol]) -> list[GenresDTO] | None:
        return await service.get_all_genres()

    @post("/")
    @inject
    async def create_genre(self, service: FromDishka[GenreProtocol], data: WriteGenreDTO) -> GenresDTO:
        return await service.create_genre(data)
