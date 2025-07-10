from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import OperationSchema, WalletSchema
from src.usecases import WalletUseCase


class OperationType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class InvalidOperationSchema(BaseModel):
    """
    Invalid operation
    """

    operation_type: str
    amount: Decimal


@pytest.mark.asyncio
async def test_get_all_wallets(wallet_usecase: WalletUseCase, session: AsyncSession):
    wallet1 = await wallet_usecase.create_wallet()
    wallet2 = await wallet_usecase.create_wallet()

    wallets = await wallet_usecase.get_all_wallets()

    assert len(wallets) >= 2
    assert any(w.uuid == wallet1.uuid for w in wallets)
    assert any(w.uuid == wallet2.uuid for w in wallets)
    assert all(isinstance(w, WalletSchema) for w in wallets)


@pytest.mark.asyncio
async def test_get_wallet_balance(wallet_usecase: WalletUseCase):
    wallet = await wallet_usecase.create_wallet()
    await wallet_usecase.change_wallet_balance(
        wallet.uuid,
        OperationSchema(
            operation_type=OperationType.DEPOSIT.value, amount=Decimal("100.50")
        ),
    )

    balance = await wallet_usecase.get_wallet_balance(wallet.uuid)
    assert balance.balance == Decimal("100.50")


@pytest.mark.asyncio
async def test_create_wallet(wallet_usecase: WalletUseCase):
    wallet = await wallet_usecase.create_wallet()

    assert isinstance(wallet, WalletSchema)
    assert wallet.balance == Decimal("0")
    assert isinstance(wallet.uuid, UUID)


@pytest.mark.asyncio
async def test_deposit_operation(wallet_usecase: WalletUseCase):
    wallet = await wallet_usecase.create_wallet()
    operation = OperationSchema(
        operation_type=OperationType.DEPOSIT.value, amount=Decimal("50.25")
    )

    balance = await wallet_usecase.change_wallet_balance(wallet.uuid, operation)
    assert balance.balance == Decimal("50.25")

    balance = await wallet_usecase.change_wallet_balance(wallet.uuid, operation)
    assert balance.balance == Decimal("100.50")


@pytest.mark.asyncio
async def test_withdraw_operation_success(wallet_usecase: WalletUseCase):
    wallet = await wallet_usecase.create_wallet()
    await wallet_usecase.change_wallet_balance(
        wallet.uuid,
        OperationSchema(
            operation_type=OperationType.DEPOSIT.value, amount=Decimal("100")
        ),
    )

    balance = await wallet_usecase.change_wallet_balance(
        wallet.uuid,
        OperationSchema(
            operation_type=OperationType.WITHDRAW.value, amount=Decimal("30.75")
        ),
    )

    assert balance.balance == Decimal("69.25")


@pytest.mark.asyncio
async def test_withdraw_insufficient_funds(wallet_usecase: WalletUseCase):
    wallet = await wallet_usecase.create_wallet()

    with pytest.raises(ValueError) as exc:
        await wallet_usecase.change_wallet_balance(
            wallet.uuid,
            OperationSchema(
                operation_type=OperationType.WITHDRAW.value, amount=Decimal("10")
            ),
        )

    assert "Insufficient funds" in str(exc)


@pytest.mark.asyncio
async def test_invalid_operation_type(wallet_usecase: WalletUseCase):
    wallet = await wallet_usecase.create_wallet()

    with pytest.raises(ValueError) as exc:
        invalid_operation = InvalidOperationSchema(
            operation_type="INVALID", amount=Decimal("10")
        )
        await wallet_usecase.change_wallet_balance(wallet.uuid, invalid_operation)

    assert "Operation type should be 'DEPOSIT' or 'WITHDRAW'" in str(exc)


@pytest.mark.asyncio
async def test_negative_amount(wallet_usecase: WalletUseCase):
    wallet = await wallet_usecase.create_wallet()  # balance = 0

    with pytest.raises(ValueError) as exc:
        invalid_operation = InvalidOperationSchema(
            operation_type=OperationType.DEPOSIT.value, amount=Decimal("-10")
        )
        await wallet_usecase.change_wallet_balance(wallet.uuid, invalid_operation)

    assert "Operation amount should be greater than 0" in str(exc)


@pytest.mark.asyncio
async def test_nonexistent_wallet(wallet_usecase: WalletUseCase):
    non_existent_uuid = uuid4()

    with pytest.raises(NoResultFound):
        await wallet_usecase.get_wallet_balance(non_existent_uuid)
