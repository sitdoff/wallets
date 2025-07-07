from fastapi import APIRouter

from src.api.v1 import router as v1_router
from src.config import settings

router = APIRouter(prefix=settings.api.api_prefix)
router.include_router(v1_router)
