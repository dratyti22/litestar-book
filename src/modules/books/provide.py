from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.books.repository import GenreRepository
from src.modules.books.service import GenresService


class GenreRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def genre_repo(
        self, session: AsyncSession
    ) -> GenreRepository:
        return GenreRepository(session)

class GenreServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def genre_service(
        self, repo: GenreRepository
    ) -> GenresService:
        return GenresService(repo)

class GenreProviders(Provider):
    @provide(scope=Scope.REQUEST)
    def genre_repo(self, session: AsyncSession) -> GenreRepository:
        return GenreRepository(session)

    @provide(scope=Scope.REQUEST)
    def genre_service(self, repo: GenreRepository) -> GenresService:
        return GenresService(repo)