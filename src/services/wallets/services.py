from decimal import Decimal
from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import WalletModel
from src.repositories import WalletRepository
from src.utils.base_service import BaseService


class WalletService(BaseService):
    def __init__(self, session: AsyncSession):
        self.repository = WalletRepository(session)

    async def get_all_wallets(self) -> Sequence[WalletModel]:
        return await self.repository.get_all()

    async def get_wallet(self, uuid: UUID) -> WalletModel:
        return await self.repository.get_by_uuid(uuid)

    async def create_wallet(self) -> WalletModel:
        return await self.repository.create()

    async def increase_balance(self, uuid: UUID, amount: Decimal) -> WalletModel:
        wallet: WalletModel = await self.repository.get_by_uuid(uuid, for_update=True)
        wallet.balance += amount
        return wallet

    async def decrease_balance(self, uuid: UUID, amount: Decimal) -> WalletModel:
        wallet: WalletModel = await self.repository.get_by_uuid(uuid, for_update=True)
        if wallet.balance < amount:
            raise ValueError("Insufficient funds")
        wallet.balance -= amount
        return wallet
