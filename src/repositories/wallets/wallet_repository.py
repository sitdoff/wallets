from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import WalletModel
from src.utils import BaseRepository


class WalletRepository(BaseRepository):
    model = WalletModel

    async def create(self) -> WalletModel:  # type: ignore
        wallet = WalletModel()
        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)
        return wallet

    async def get_all(self) -> Sequence[WalletModel]:  # type: ignore
        statement = select(self.model)
        result = await self.session.execute(statement)
        wallets = result.scalars().all()
        return wallets

    async def get_by_uuid(self, uuid: UUID, for_update: bool = False) -> WalletModel:  # type: ignore
        return await self.get_by_id(id=str(uuid), for_update=for_update)

    async def get_by_id(self, id: str, for_update: bool = False) -> WalletModel:  # type: ignore
        statement = select(self.model).where(self.model.uuid == id)
        if for_update:
            statement = statement.with_for_update()
        result = await self.session.execute(statement)
        wallet = result.scalar_one_or_none()
        if wallet is None:
            raise NoResultFound(f"Wallet with uuid={id} not found")
        return wallet
