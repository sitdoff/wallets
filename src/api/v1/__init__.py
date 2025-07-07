from fastapi import APIRouter

from src.api.v1.wallets import router as wallets_router
from src.config import settings

router = APIRouter(prefix=settings.api.v1_prefix)
router.include_router(wallets_router)
