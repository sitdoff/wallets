from fastapi import APIRouter

from src.config import settings

router = APIRouter(prefix=settings.api.v1_prefix)
