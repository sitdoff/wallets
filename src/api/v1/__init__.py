from fastapi import APIRouter

from src.api.v1.example_app import router as example_router
from src.config import settings

router = APIRouter(prefix=settings.api.v1_prefix)
router.include_router(example_router)
