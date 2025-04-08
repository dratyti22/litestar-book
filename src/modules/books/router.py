from typing import Any

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import post, HttpMethod, route, patch, delete, get, Request
from litestar.controller import Controller
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from litestar.security.jwt import Token
from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.guards import admin_user_guard
from src.modules.books.model import BookDb
from src.modules.books.protocols import GenreProtocol, BookProtocol
from src.modules.books.schema import GenresDTO, WriteGenreDTO, WriteBookDTO, PatchBookDTO, \
    BookResponseDTO, WriteBookRequest, PatchBookRequest, BookDTO
from src.modules.users.model import UserDb


class GenreController(Controller):
    path = "/genre"

    @route(http_method=HttpMethod.GET, path="/", exclude_from_auth=True, cached=3600)
    @inject
    async def get_all_genres(self, service: FromDishka[GenreProtocol]) -> list[GenresDTO] | None:
        return await service.get_all_genres()

    @post("/", guards=[admin_user_guard])
    @inject
    async def create_genre(self, service: FromDishka[GenreProtocol], data: WriteGenreDTO) -> GenresDTO:
        return await service.create_genre(data)


class BookController(Controller):
    path = "/book"

    @get("/", exclude_from_auth=True, cached=3600, return_dto=BookResponseDTO)
    @inject
    async def get_all_books(
        self,
        service: FromDishka[BookProtocol]
    ) -> list[BookDb]:
        books = await service.get_all_books()
        book_dtos = [BookDTO(
            id=book.id,
            title=book.title,
            slug=book.slug,
            price=book.price,
            description=book.description,
            genre_id=book.genre_id,
            user_id=book.user_id
        ) for book in books]

        return book_dtos

    @post("/", dto=WriteBookDTO, return_dto=BookResponseDTO)
    @inject
    async def create_book(
        self,
        service: FromDishka[BookProtocol],
        data: DTOData[WriteBookRequest],
        request: Request[UserDb, Token, Any],
    ) -> BookDb:

        try:
            book_data = data.as_builtins()
            book = await service.create_book(book_data, request.user.id)
            return BookDTO(
                id=book.id,
                title=book.title,
                slug=book.slug,
                price=book.price,
                description=book.description,
                genre_id=book.genre_id,
                user_id=book.user_id
            )
        except SQLAlchemyError:
            raise HTTPException(detail="Database error", status_code=500)
        except Exception:
            raise HTTPException(detail="Internal server error", status_code=500)

    @patch("/{book_id:int}", dto=PatchBookDTO, return_dto=BookResponseDTO)
    @inject
    async def update_book(
        self,
        service: FromDishka[BookProtocol],
        book_id: int,
        data: DTOData[PatchBookRequest],
        request: Request[UserDb, Token, Any]
    ) -> BookDb:
        book = await service.update_book(book_id, data.as_builtins(), request.user.id)
        return BookDTO(
            id=book.id,
            title=book.title,
            slug=book.slug,
            price=book.price,
            description=book.description,
            genre_id=book.genre_id,
            user_id=book.user_id
        )

    @delete("/{book_id:int}")
    @inject
    async def delete_book(
        self,
        service: FromDishka[BookProtocol],
        book_id: int,
        request: Request[UserDb, Token, Any]
    ) -> None:
        await service.delete_book(book_id, request.user.id)
