from abc import ABC, abstractmethod


class AbstractSerice(ABC):
    pass


class BaseService(AbstractSerice):
    def __init__(self, repository):
        self.repository = repository
