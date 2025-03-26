from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from src.settings import Settings


def new_session_maker(settings: Settings) -> async_sessionmaker[AsyncSession]:
    database_url = 'postgresql+psycopg://{user}:{password}@{host}:{port}/{database}'.format(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.POSTGRES_DB,
    )

    engine = create_async_engine(
        database_url,
        pool_size=15,
        max_overflow=15,
        connect_args={
            "connect_timeout": 5,
        },
    )
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
