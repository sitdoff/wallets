from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from src.config import settings


class DatabaseManager:
    """
    Класс для взаимодействия с базой данных.
    """

    def __init__(
        self,
        url: str = settings.db.url,
        echo: bool = settings.db.echo,
        echo_pool: bool = settings.db.echo_pool,
        pool_size: int = settings.db.pool_size,
        max_overflow: int = settings.db.max_overflow,
    ):
        """
        При инициализации экземпляра класса создается
        соединение с базой и фабрика сессий.
        """
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def dispose(self) -> None:
        """
        Метод для выключения соединения с базой.
        """
        await self.engine.dispose()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Метод-герератор возвращающий объект сессии.
        """
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseManager()
