from uuid import UUID

import pytest
from sqlalchemy.exc import NoResultFound

from src.models import WalletModel


@pytest.mark.asyncio
async def test_create_wallet(repository):
    wallet = await repository.create()

    assert isinstance(wallet, WalletModel)
    assert isinstance(wallet.uuid, str)


@pytest.mark.asyncio
async def test_get_all_wallets_len(repository):
    wallets = await repository.get_all()
    assert len(wallets) == 1


@pytest.mark.asyncio
async def test_get_all_wallets_after_create(repository):
    await repository.create()
    await repository.create()
    wallets = await repository.get_all()

    assert len(wallets) >= 3
    assert all(isinstance(wallet, WalletModel) for wallet in wallets)


@pytest.mark.asyncio
async def test_get_by_id_success(repository):
    wallet = await repository.create()

    found = await repository.get_by_id(str(wallet.uuid))
    assert found.uuid == wallet.uuid


@pytest.mark.asyncio
async def test_get_by_uuid_success(repository):
    wallet = await repository.create()

    found = await repository.get_by_uuid(wallet.uuid)
    assert found.uuid == wallet.uuid


@pytest.mark.asyncio
async def test_get_by_id_not_found(repository):
    with pytest.raises(NoResultFound):
        await repository.get_by_id("ffffffff-ffff-ffff-ffff-ffffffffffff")


@pytest.mark.asyncio
async def test_get_by_uuid_not_found(repository):
    with pytest.raises(NoResultFound):
        await repository.get_by_uuid(UUID("ffffffff-ffff-ffff-ffff-ffffffffffff"))
