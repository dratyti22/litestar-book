from litestar.exceptions import HTTPException, PermissionDeniedException
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.books.protocols import GenreProtocol, BookProtocol
from src.modules.books.model import GenresDb, BookDb
from src.modules.books.schema import GenresDTO, WriteGenreDTO


class GenreRepository(GenreProtocol):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_all_genres(self) -> list[GenresDTO] | None:
        result = await self.db_session.execute(select(GenresDb))
        genres = result.scalars().all()
        return [GenresDTO(id=genre.id, name=genre.name, slug=genre.slug) for genre in genres]

    async def create_genre(self, data: WriteGenreDTO) -> GenresDTO:
        slug = slugify(data.name)
        genre = GenresDb(name=data.name, slug=slug)
        self.db_session.add(genre)
        await self.db_session.commit()
        await self.db_session.refresh(genre)
        return GenresDTO(id=genre.id, name=genre.name, slug=genre.slug)


class BookRepository(BookProtocol):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_books(self) -> list[BookDb]:
        result = await self.db_session.execute(select(BookDb))
        books = result.scalars().all()
        return books

    async def create_book(self, data: dict, user_id: int) -> BookDb:
        try:
            slug = slugify(data.get("title"))
            book = BookDb(
                title=data.get("title"),
                slug=slug,
                price=data.get("price"),
                description=data.get("description"),
                genre_id=data.get("genre_id"),
                user_id=user_id
            )

            self.db_session.add(book)
            await self.db_session.commit()
            await self.db_session.refresh(book)
            return book
        except Exception:
            await self.db_session.rollback()
            raise

    async def update_book(self, book_id: int, data: dict, user_id: int) -> BookDb:
        result = await self.db_session.execute(select(BookDb).where(BookDb.id == book_id))
        book = result.scalars().first()
        if book is None:
            raise HTTPException(
                status_code=404, detail="Book not found"
            )
        if book.user_id != user_id:
            raise PermissionDeniedException("Not your book")
        for field, value in data.items():
            if value is not None and hasattr(book, field):
                setattr(book, field, value)

        if data.get("title"):
            book.slug = slugify(data.get("title"))

        await self.db_session.commit()
        await self.db_session.refresh(book)
        return book

    async def delete_book(self, book_id: int, user_id: int) -> bool:
        result = await self.db_session.execute(select(BookDb).where(BookDb.id == book_id))
        book = result.scalars().first()
        if book is None:
            raise HTTPException(
                status_code=404, detail="Book not found"
            )
        if book.user_id != user_id:
            raise PermissionDeniedException("Not your book")
        await self.db_session.delete(book)
        await self.db_session.commit()
        return True
