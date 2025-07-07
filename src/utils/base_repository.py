from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def save(self):
        pass

    @abstractmethod
    async def get_all(self):
        pass


class BaseRepository(AbstractRepository):
    def __init__(self, model):
        self.model = model
