from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.wallets.docs import docs as wallets_docs
from src.database import db_helper
from src.dependencies import get_usecase
from src.schemas import OperationSchema, WalletBalance, WalletSchema
from src.usecases import WalletUseCase

router = APIRouter()


@router.get("/all", **wallets_docs["all"])
async def get_all_wallets(
    usecase: Annotated[WalletUseCase, Depends(get_usecase)],
) -> list[WalletSchema]:
    return await usecase.get_all_wallets()


@router.get("/{uuid}", **wallets_docs["balance"])
async def get_balance(
    uuid: Annotated[UUID, Path(description="Уникальный идентификатор кошелька")],
    usecase: Annotated[WalletUseCase, Depends(get_usecase)],
) -> WalletBalance:
    try:
        return await usecase.get_wallet_balance(uuid)
    except NoResultFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/create", **wallets_docs["create"])
async def create_wallet(
    usecase: Annotated[WalletUseCase, Depends(get_usecase)],
) -> WalletSchema:
    return await usecase.create_wallet()


@router.post("/{uuid}/operation", **wallets_docs["operation"])
async def change_balance(
    uuid: Annotated[UUID, Path(description="Уникальный идентификатор кошелька")],
    operation_scheme: Annotated[OperationSchema, Body()],
    usecase: Annotated[WalletUseCase, Depends(get_usecase)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> WalletBalance:
    async with session.begin():
        try:
            return await usecase.change_wallet_balance(uuid, operation_scheme)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
            )
        except NoResultFound as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
