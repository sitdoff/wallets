from fastapi import APIRouter

from src.config import settings

router = APIRouter(
    prefix=settings.example_app.router_prefix,
    tags=["example-tag"],
)


@router.get("/example-endpoint")
async def example_app() -> str:
    return "example app"
