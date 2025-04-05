from typing import AsyncIterator

from dishka import Provider, Scope, provide, from_context
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.database import new_session_maker
from src.modules.books.protocols import GenreProtocol, BookProtocol
from src.modules.books.repository import GenreRepository, BookRepository
from src.modules.users.model import UserDb
from src.modules.users.protocol import UserProtocol
from src.modules.users.repository import UserRepository
from src.settings import Settings


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> UserDb | None:
        try:
            result = await self.session.execute(
                select(UserDb).where(UserDb.id == user_id))
            return result.scalar_one_or_none()
        except Exception as e:
            self.session.logger.error(f"AuthService error: {str(e)}")
            return None


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, settings: Settings) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(settings)

    @provide(scope=Scope.REQUEST)
    # @asynccontextmanager
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session
            await session.commit()
        # finally:
        #     await session.close()

    # genre_gateway = provide(GenreRepository, scope=Scope.REQUEST, provides=GenreProtocol)
    @provide(provides=GenreProtocol, scope=Scope.REQUEST)
    async def get_genre_repo(self, session: AsyncSession) -> GenreProtocol:
        return GenreRepository(session)

    @provide(scope=Scope.REQUEST)
    async def get_auth_service(self, session: AsyncSession) -> AuthService:
        return AuthService(session)

    @provide(provides=UserProtocol, scope=Scope.REQUEST)
    async def get_user_repo(self, session: AsyncSession) -> UserProtocol:
        return UserRepository(session)

    @provide(provides=BookProtocol, scope=Scope.REQUEST)
    async def get_book_repo(self, session: AsyncSession) -> BookProtocol:
        try:
            return BookRepository(session)
        except Exception as e:
            session.logger.error(f"Error creating BookRepository: {str(e)}")
            print(f"Error creating BookRepository {str(e)}")
            raise
