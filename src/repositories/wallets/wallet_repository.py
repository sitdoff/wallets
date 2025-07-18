from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.models import WalletModel
from src.repositories import BaseRepository


class WalletRepository(BaseRepository):
    """
    Репозиторий для взаимодействия с базой данных
    """

    model = WalletModel

    async def create(self) -> WalletModel:
        """
        Создание кошелька в базе данных
        """
        wallet = WalletModel()
        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)
        return wallet

    async def get_all(self) -> Sequence[WalletModel]:
        """
        Получение списка существующий кошельков из базы данных
        """
        statement = select(self.model)
        result = await self.session.execute(statement)
        wallets = result.scalars().all()
        return wallets

    async def get_by_uuid(self, uuid: UUID, for_update: bool = False) -> WalletModel:
        """
        Получение кошелька по uuid из базы данных
        """
        return await self.get_by_id(id=uuid, for_update=for_update)

    async def get_by_id(self, id: UUID, for_update: bool = False) -> WalletModel:
        """
        Получение кошелька по primary key из базы данных
        """
        statement = select(self.model).where(self.model.uuid == id)
        if for_update:
            statement = statement.with_for_update()
        result = await self.session.execute(statement)
        wallet = result.scalar_one_or_none()
        if wallet is None:
            raise NoResultFound(f"Wallet with uuid={id} not found")
        return wallet
