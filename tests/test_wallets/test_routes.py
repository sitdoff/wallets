from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy.exc import NoResultFound

from src.main import app
from src.schemas import WalletBalance, WalletSchema
from src.usecases import get_usecase

wallet1 = WalletSchema(uuid=str(uuid4()), balance=Decimal("100.00"))
wallet2 = WalletSchema(uuid=str(uuid4()), balance=Decimal("50.00"))
wallet3 = WalletSchema(uuid=str(uuid4()), balance=Decimal("0.00"))


@pytest.fixture
def mock_wallet_usecase():
    mock = MagicMock()
    mock.get_all_wallets = AsyncMock(return_value=[wallet1, wallet2])
    # mock.get_wallet_balance = AsyncMock(return_value={"balance": wallet1.balance})
    mock.get_wallet_balance = AsyncMock(
        side_effect=[
            {"balance": wallet1.balance},
            NoResultFound("Wallet with uuid={id} not found"),
        ]
    )
    mock.create_wallet = AsyncMock(return_value=wallet3)
    mock.change_wallet_balance = AsyncMock(
        side_effect=[
            WalletBalance(balance=wallet2.balance),
            NoResultFound("Wallet with uuid={id} not found"),
        ]
    )
    return mock


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test/api/v1"
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def override_usecase(mock_wallet_usecase):
    app.dependency_overrides[get_usecase] = lambda: mock_wallet_usecase
    yield
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_get_all_wallets(async_client: AsyncClient, mock_wallet_usecase):
    response = await async_client.get("/wallets/all")
    assert response.status_code == 200
    assert response.json() == [
        {"uuid": wallet1.uuid, "balance": str(wallet1.balance)},
        {"uuid": wallet2.uuid, "balance": str(wallet2.balance)},
    ]
    mock_wallet_usecase.get_all_wallets.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_balance(async_client: AsyncClient, mock_wallet_usecase):
    response: Response = await async_client.get(f"/wallets/{wallet1.uuid}")
    assert response.status_code == 200
    mock_wallet_usecase.get_wallet_balance.assert_awaited_once()

    response: Response = await async_client.get(f"/wallets/{uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet with uuid={id} not found"}


@pytest.mark.asyncio
async def test_create_wallet(async_client: AsyncClient, mock_wallet_usecase):
    response: Response = await async_client.post("/wallets/create")
    assert response.status_code == 201
    mock_wallet_usecase.create_wallet.assert_awaited_once()


@pytest.mark.asyncio
async def test_change_balance(async_client: AsyncClient, mock_wallet_usecase):
    body = {
        "operation_type": "DEPOSIT",
        "amount": "123.45",
    }
    response: Response = await async_client.post(
        f"wallets/{wallet2.uuid}/operation", json=body
    )
    assert response.status_code == 200
    mock_wallet_usecase.change_wallet_balance.assert_awaited_once()

    response: Response = await async_client.post(
        f"wallets/{uuid4()}/operation", json=body
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet with uuid={id} not found"}
