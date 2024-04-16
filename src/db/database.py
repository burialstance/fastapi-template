from asyncio import current_task
from contextlib import asynccontextmanager

from advanced_alchemy import base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)


class Database:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.url = url

        self.async_engine = create_async_engine(
            url,
            pool_pre_ping=True,
            echo=echo
        )

        self.async_session_maker = async_sessionmaker(
            self.async_engine,
            expire_on_commit=False,
            autoflush=False,
            future=True,
        )

        self.session_factory = async_scoped_session(
            self.async_session_maker,
            scopefunc=current_task,
        )

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except IntegrityError as exception:
            await session.rollback()
        finally:
            await session.close()

    async def create_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(base.UUIDAuditBase.metadata.create_all)
