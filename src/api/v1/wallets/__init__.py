from fastapi import APIRouter

from src.api.v1.wallets.router import router as wallets_router
from src.config import settings

router = APIRouter(prefix=settings.api.wallets.app_prefix, tags=["wallets"])
router.include_router(wallets_router)
