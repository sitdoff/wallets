from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import WalletModel
from src.schemas import OperationSchema, WalletBalance, WalletSchema
from src.services import WalletService
from src.usecases import BaseUseCase
from src.utils import transactional


class WalletUseCase(BaseUseCase):
    """
    Класс-оркестратор сервисов.
    """

    def __init__(self, session: AsyncSession, service: WalletService):
        self.session = session
        self.service = service

    async def get_all_wallets(self) -> list[WalletSchema]:
        """
        Получение данных о всех кошельках из базы данных.
        """
        wallets: Sequence[WalletModel] = await self.service.get_all_wallets()
        return [
            WalletSchema(uuid=wallet.uuid, balance=wallet.balance) for wallet in wallets  # type: ignore[arg-type]
        ]

    async def get_wallet_balance(self, uuid: UUID) -> WalletBalance:
        """
        Получение данных о кошельке
        """
        wallet: WalletModel = await self.service.get_wallet(uuid)
        return WalletBalance(balance=wallet.balance)

    async def create_wallet(self) -> WalletSchema:
        """
        Создание кошелька
        """
        wallet: WalletModel = await self.service.create_wallet()
        return WalletSchema(uuid=wallet.uuid, balance=wallet.balance)  # type: ignore[arg-type]

    @transactional
    async def change_wallet_balance(
        self,
        uuid: UUID,
        operation_scheme: OperationSchema,
    ) -> WalletBalance:
        """
        Изменение баланса кошелька
        """
        if operation_scheme.amount <= 0:
            raise ValueError("Operation amount should be greater than 0")
        if operation_scheme.operation_type == "DEPOSIT":
            await self.service.increase_balance(uuid, operation_scheme.amount)
        elif operation_scheme.operation_type == "WITHDRAW":
            await self.service.decrease_balance(uuid, operation_scheme.amount)
        else:
            raise ValueError("Operation type should be 'DEPOSIT' or 'WITHDRAW'")
        return await self.get_wallet_balance(uuid)
