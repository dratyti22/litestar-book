from typing import AsyncIterable

from dishka import Provider, Scope, provide, from_context
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.database import new_session_maker
from src.modules.books.protocols import GenreProtocol
from src.modules.books.repository import GenreRepository
from src.modules.users.protocol import UserProtocol
from src.modules.users.repository import UserRepository
from src.settings import Settings


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, settings: Settings) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(settings)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session
            await session.commit()

    # genre_gateway = provide(GenreRepository, scope=Scope.REQUEST, provides=GenreProtocol)
    @provide(provides=GenreProtocol, scope=Scope.REQUEST)
    async def get_genre_repo(self, session: AsyncSession) -> GenreProtocol:
        return GenreRepository(session)

    @provide(provides=UserProtocol, scope=Scope.REQUEST)
    async def get_user_repo(self, session: AsyncSession) -> UserProtocol:
        return UserRepository(session)
