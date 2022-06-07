from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import Config

Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = None
        self._session = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self, db_config):
        self._engine = create_async_engine(
            db_config,
            future=True,
            echo=False,
        )

        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


def get_db():
    db = AsyncDatabaseSession()
    db.init(Config.DB_CONFIG)
    return db
