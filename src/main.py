from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import router as api_router
from src.config import settings
from src.database import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Функция содержит в себе действия, которые должны быть
    выполнены до старта приложения и до завершения его работы.
    """
    # startup
    yield
    # shutdown
    print("Disposing database connection...")
    await db_helper.dispose()
    print("Connection disposed")


app = FastAPI(
    prefix=settings.api.api_prefix,
    lifespan=lifespan,
)
app.include_router(api_router)
