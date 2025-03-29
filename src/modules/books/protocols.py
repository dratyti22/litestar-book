from abc import abstractmethod
from typing import Protocol

from src.modules.books.schema import GenresDTO, WriteGenreDTO


class GenreProtocol(Protocol):
    @abstractmethod
    async def get_all_genres(self) -> list[GenresDTO] | None:
        ...

    @abstractmethod
    async def create_genre(self, data: WriteGenreDTO) -> GenresDTO:
        ...
