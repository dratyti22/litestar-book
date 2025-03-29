from src.modules.books.repository import GenreRepository
from src.modules.books.schema import WriteGenreDTO, GenresDTO


class GenresService:
    def __init__(self, repository: GenreRepository) -> None:
        self.repository = repository

    async def get_all_genres(self) -> list[GenresDTO] | None:
        return await self.repository.get_all_genres()

    async def create_genre(self, data: WriteGenreDTO) -> GenresDTO:
        return await self.repository.create_genre(data)
