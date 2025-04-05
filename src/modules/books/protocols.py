from abc import abstractmethod
from typing import Protocol

from src.modules.books.model import BookDb
from src.modules.books.schema import GenresDTO, WriteGenreDTO


class GenreProtocol(Protocol):
    @abstractmethod
    async def get_all_genres(self) -> list[GenresDTO] | None:
        ...

    @abstractmethod
    async def create_genre(self, data: WriteGenreDTO) -> GenresDTO:
        ...


class BookProtocol(Protocol):
    @abstractmethod
    async def get_all_books(self) -> list[BookDb]:
        ...
    @abstractmethod
    async def create_book(self, data: dict, user_id: int) -> BookDb:
        ...

    @abstractmethod
    async def update_book(self, book_id: int, data: dict, user_id: int) -> BookDb:
        ...

    @abstractmethod
    async def delete_book(self, book_id: int, user_id: int) -> bool:
        ...
