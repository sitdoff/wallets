from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.models.wallets import WalletModel
from src.repositories.wallets.wallet_repository import WalletRepository
from src.schemas import OperationSchema, WalletBalance, WalletSchema
from src.services import WalletService
from src.usecases import WalletUseCase

router = APIRouter()


@router.get("/all")
async def get_all_wallets(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> list[WalletSchema]:
    usecase = WalletUseCase(session=session, service=WalletService(session))
    return await usecase.get_all_wallets()


@router.get("/{uuid}")
async def get_balance(
    uuid: Annotated[UUID, Path()],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> WalletBalance:
    usecase = WalletUseCase(session=session, service=WalletService(session))
    return await usecase.get_wallet_balance(uuid)


@router.post("/create")
async def create_wallet(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> WalletSchema:
    usecase = WalletUseCase(session=session, service=WalletService(session))
    return await usecase.create_wallet()


@router.post("/{uuid}/operation")
async def change_balance(
    uuid: Annotated[UUID, Path()],
    operation_scheme: Annotated[OperationSchema, Body()],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> WalletBalance:
    usecase = WalletUseCase(session=session, service=WalletService(session))
    return await usecase.change_wallet_balance(uuid, operation_scheme)
