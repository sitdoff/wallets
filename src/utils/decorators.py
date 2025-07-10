from functools import wraps

from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound


def transactional(func):
    """
    Декоратор для автоматического управления транзакциями
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self.session.in_transaction():
            return await func(self, *args, **kwargs)
        async with self.session.begin():
            return await func(self, *args, **kwargs)

    return wrapper


def handle_exceptions(func):
    """
    Декоратор для обработки ошибок
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except NoResultFound as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
            )

    return wrapper
