from abc import ABC, abstractmethod
from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):

    @abstractmethod
    async def create(self) -> Any:
        pass

    @abstractmethod
    async def get_all(self) -> Sequence[Any]:
        pass

    @abstractmethod
    async def get_by_id(self, id) -> Any:
        pass


class BaseRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
