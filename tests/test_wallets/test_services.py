from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy.exc import NoResultFound

from src.models import WalletModel
from src.services import WalletService


@pytest.mark.asyncio
async def test_create_wallet(service: WalletService):
    wallet = await service.create_wallet()

    assert isinstance(wallet, WalletModel)
    assert wallet.uuid is not None
    assert wallet.balance == Decimal("0")
    assert isinstance(wallet.uuid, UUID)


@pytest.mark.asyncio
async def test_get_all_wallets(service: WalletService):

    wallet1 = await service.create_wallet()
    wallet2 = await service.create_wallet()

    wallets = await service.get_all_wallets()

    assert len(wallets) >= 2
    assert any(w.uuid == wallet1.uuid for w in wallets)
    assert any(w.uuid == wallet2.uuid for w in wallets)
    assert all(isinstance(w, WalletModel) for w in wallets)


@pytest.mark.asyncio
async def test_get_wallet(service: WalletService):
    created_wallet = await service.create_wallet()

    retrieved_wallet = await service.get_wallet(created_wallet.uuid)  # type: ignore[arg-type]

    assert retrieved_wallet.uuid == created_wallet.uuid
    assert retrieved_wallet.balance == created_wallet.balance


@pytest.mark.asyncio
async def test_increase_balance(service: WalletService):
    wallet = await service.create_wallet()

    updated_wallet = await service.increase_balance(wallet.uuid, Decimal("100.50"))  # type: ignore[arg-type]

    assert updated_wallet.balance == Decimal("100.50")

    db_wallet = await service.get_wallet(wallet.uuid)  # type: ignore[arg-type]
    assert db_wallet.balance == Decimal("100.50")


@pytest.mark.asyncio
async def test_decrease_balance_success(service: WalletService):
    wallet = await service.create_wallet()
    await service.increase_balance(wallet.uuid, Decimal("100"))  # type: ignore[arg-type]

    updated_wallet = await service.decrease_balance(wallet.uuid, Decimal("30.25"))  # type: ignore[arg-type]

    assert updated_wallet.balance == Decimal("69.75")

    db_wallet = await service.get_wallet(wallet.uuid)  # type: ignore[arg-type]
    assert db_wallet.balance == Decimal("69.75")


@pytest.mark.asyncio
async def test_decrease_balance_insufficient_funds(service: WalletService):
    wallet = await service.create_wallet()

    with pytest.raises(ValueError) as exc:
        await service.decrease_balance(wallet.uuid, Decimal("10"))  # type: ignore[arg-type]

    assert "Insufficient funds" in str(exc.value)

    db_wallet = await service.get_wallet(wallet.uuid)  # type: ignore[arg-type]
    assert db_wallet.balance == Decimal("0")


@pytest.mark.asyncio
async def test_balance_operations_sequence(service: WalletService):
    wallet = await service.create_wallet()

    await service.increase_balance(wallet.uuid, Decimal("100"))  # type: ignore[arg-type]
    await service.decrease_balance(wallet.uuid, Decimal("40"))  # type: ignore[arg-type]
    await service.increase_balance(wallet.uuid, Decimal("20"))  # type: ignore[arg-type]

    final_balance = (await service.get_wallet(wallet.uuid)).balance  # type: ignore[arg-type]
    assert final_balance == Decimal("80")


@pytest.mark.asyncio
async def test_get_nonexistent_wallet(service: WalletService):
    non_existent_uuid = uuid4()

    with pytest.raises(NoResultFound):
        await service.get_wallet(non_existent_uuid)
