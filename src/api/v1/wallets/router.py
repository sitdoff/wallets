from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.wallets.docs import docs as wallets_docs
from src.database import db_helper
from src.schemas import OperationSchema, WalletBalance, WalletSchema
from src.services import WalletService
from src.usecases import WalletUseCase

router = APIRouter()


@router.get("/all", **wallets_docs["all"])
async def get_all_wallets(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> list[WalletSchema]:
    usecase = WalletUseCase(session=session, service=WalletService(session))
    return await usecase.get_all_wallets()


@router.get("/{uuid}", **wallets_docs["balance"])
async def get_balance(
    uuid: Annotated[UUID, Path(description="Уникальный идентификатор кошелька")],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> WalletBalance:
    usecase = WalletUseCase(session=session, service=WalletService(session))
    return await usecase.get_wallet_balance(uuid)


@router.post("/create", **wallets_docs["create"])
async def create_wallet(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> WalletSchema:
    usecase = WalletUseCase(session=session, service=WalletService(session))
    return await usecase.create_wallet()


@router.post("/{uuid}/operation", **wallets_docs["operation"])
async def change_balance(
    uuid: Annotated[UUID, Path(description="Уникальный идентификатор кошелька")],
    operation_scheme: Annotated[OperationSchema, Body()],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> WalletBalance:
    usecase = WalletUseCase(session=session, service=WalletService(session))
    async with session.begin():
        return await usecase.change_wallet_balance(uuid, operation_scheme)
