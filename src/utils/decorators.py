# decorators.py
import logging
from functools import wraps
from typing import Optional


def transactional(func):
    """
    Декоратор для автоматического управления транзакциями
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self.session.in_transaction():
            return await func(self, *args, **kwargs)
        else:
            async with self.session.begin():
                return await func(self, *args, **kwargs)

    return wrapper
