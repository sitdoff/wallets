from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy.exc import NoResultFound

from src.config import settings
from src.dependencies import get_usecase
from src.main import app
from src.schemas import WalletBalance, WalletSchema

wallet1 = WalletSchema(uuid=uuid4(), balance=Decimal("100.00"))
wallet2 = WalletSchema(uuid=uuid4(), balance=Decimal("50.00"))
wallet3 = WalletSchema(uuid=uuid4(), balance=Decimal("0.00"))


@pytest.fixture
def mock_wallet_usecase():
    mock = MagicMock()
    mock.get_all_wallets = AsyncMock(return_value=[wallet1, wallet2])
    mock.get_wallet_balance = AsyncMock(
        side_effect=[
            {"balance": wallet1.balance},
            NoResultFound("Handled NoResultFound"),
        ]
    )
    mock.create_wallet = AsyncMock(return_value=wallet3)
    mock.change_wallet_balance = AsyncMock(
        side_effect=[
            WalletBalance(balance=wallet2.balance),
            NoResultFound("Handled NoResultFound"),
            ValueError("Handled ValueError"),
        ]
    )
    return mock


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url=f"http://test{settings.api.api_prefix}{settings.api.v1_prefix}",
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def override_usecase(mock_wallet_usecase):
    app.dependency_overrides[get_usecase] = lambda: mock_wallet_usecase
    yield
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_get_all_wallets(async_client: AsyncClient, mock_wallet_usecase):
    response = await async_client.get(f"{settings.api.wallets.app_prefix}/all")
    assert response.status_code == 200
    assert response.json() == [
        {"uuid": str(wallet1.uuid), "balance": str(wallet1.balance)},
        {"uuid": str(wallet2.uuid), "balance": str(wallet2.balance)},
    ]
    mock_wallet_usecase.get_all_wallets.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_balance(async_client: AsyncClient, mock_wallet_usecase):
    response: Response = await async_client.get(
        f"{settings.api.wallets.app_prefix}/{wallet1.uuid}"
    )
    assert response.status_code == 200
    mock_wallet_usecase.get_wallet_balance.assert_awaited_once()

    response: Response = await async_client.get(
        f"{settings.api.wallets.app_prefix}/{uuid4()}"
    )
    assert response.status_code == 404
    assert response.is_client_error == True
    assert response.json() == {"detail": "Handled NoResultFound"}


@pytest.mark.asyncio
async def test_create_wallet(async_client: AsyncClient, mock_wallet_usecase):
    response: Response = await async_client.post(
        f"{settings.api.wallets.app_prefix}/create"
    )
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
    assert response.is_client_error == True
    assert response.json() == {"detail": "Handled NoResultFound"}

    response: Response = await async_client.post(
        f"wallets/{uuid4()}/operation", json=body
    )
    assert response.status_code == 400
    assert response.is_client_error == True
    assert response.json() == {"detail": "Handled ValueError"}
