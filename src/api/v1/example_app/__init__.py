from fastapi import APIRouter

from src.api.v1.example_app.router import router as example_router
from src.config import settings

router = APIRouter(prefix=settings.example_app.app_prefix)
router.include_router(example_router)
