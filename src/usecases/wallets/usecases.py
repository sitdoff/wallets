from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import WalletModel
from src.schemas import OperationSchema, WalletBalance, WalletSchema
from src.services import WalletService
from src.utils import BaseUseCase


class WalletUseCase(BaseUseCase):
    def __init__(self, session: AsyncSession, service: WalletService):
        self.session = session
        self.service = service

    async def get_all_wallets(self) -> list[WalletSchema]:
        wallets: Sequence[WalletModel] = await self.service.get_all_wallets()
        return [
            WalletSchema(uuid=wallet.uuid, balance=wallet.balance) for wallet in wallets
        ]

    async def get_wallet_balance(self, uuid: UUID) -> WalletBalance:
        wallet: WalletModel = await self.service.get_wallet(uuid)
        return WalletBalance(balance=wallet.balance)

    async def create_wallet(self) -> WalletSchema:
        wallet: WalletModel = await self.service.create_wallet()
        return WalletSchema(uuid=wallet.uuid, balance=wallet.balance)

    async def change_wallet_balance(
        self,
        uuid: UUID,
        operation_scheme: OperationSchema,
    ) -> WalletBalance:
        async with self.session.begin():
            if operation_scheme.operation_type == "DEPOSIT":
                await self.service.increase_balance(uuid, operation_scheme.amount)
            if operation_scheme.operation_type == "WITHDRAW":
                await self.service.decrease_balance(uuid, operation_scheme.amount)
            return await self.get_wallet_balance(uuid)
