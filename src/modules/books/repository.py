from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.books.protocols import GenreProtocol
from src.modules.books.model import GenresDb
from src.modules.books.schema import GenresDTO, WriteGenreDTO


class GenreRepository(GenreProtocol):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_all_genres(self) -> list[GenresDTO] | None:
        result = await self.db_session.execute(select(GenresDb))
        genres = result.scalars().all()
        return [GenresDTO(id=genre.id, name=genre.name, slug=genre.slug) for genre in genres]

    async def create_genre(self, data: WriteGenreDTO)->GenresDTO:
        slug = slugify(data.name)
        genre = GenresDb(name=data.name, slug=slug)
        self.db_session.add(genre)
        await self.db_session.commit()
        await self.db_session.refresh(genre)
        return GenresDTO(id=genre.id, name=genre.name, slug=genre.slug)
