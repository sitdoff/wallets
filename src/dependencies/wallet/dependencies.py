from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.services import WalletService
from src.usecases import WalletUseCase


async def get_usecase(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> WalletUseCase:
    return WalletUseCase(session=session, service=WalletService(session))
