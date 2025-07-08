from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):

    @abstractmethod
    async def create(self):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, id):
        pass


class BaseRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
