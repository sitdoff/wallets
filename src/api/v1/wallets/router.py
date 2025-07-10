from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path

from src.api.v1.wallets.docs import docs as wallets_docs
from src.dependencies import get_wallet_usecase
from src.schemas import OperationSchema, WalletBalance, WalletSchema
from src.usecases import WalletUseCase
from src.utils import handle_exceptions

router = APIRouter()


@router.get("/all", **wallets_docs["all"])
@handle_exceptions
async def get_all_wallets(
    usecase: Annotated[WalletUseCase, Depends(get_wallet_usecase)],
) -> list[WalletSchema]:
    return await usecase.get_all_wallets()


@router.get("/{uuid}", **wallets_docs["balance"])
@handle_exceptions
async def get_balance(
    uuid: Annotated[UUID, Path(description="Уникальный идентификатор кошелька")],
    usecase: Annotated[WalletUseCase, Depends(get_wallet_usecase)],
) -> WalletBalance:
    return await usecase.get_wallet_balance(uuid)


@router.post("/create", **wallets_docs["create"])
@handle_exceptions
async def create_wallet(
    usecase: Annotated[WalletUseCase, Depends(get_wallet_usecase)],
) -> WalletSchema:
    return await usecase.create_wallet()


@router.post("/{uuid}/operation", **wallets_docs["operation"])
@handle_exceptions
async def change_balance(
    uuid: Annotated[UUID, Path(description="Уникальный идентификатор кошелька")],
    operation_scheme: Annotated[
        OperationSchema, Body(description="Cхема тела запроса операции")
    ],
    usecase: Annotated[WalletUseCase, Depends(get_wallet_usecase)],
) -> WalletBalance:
    return await usecase.change_wallet_balance(uuid, operation_scheme)
