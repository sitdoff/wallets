from contextlib import asynccontextmanager
from typing import Sequence

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exception: RequestValidationError):
    """
    Обработка ошибок валидации, которые возникают при создании параметров Path, Query, Body, etc.
    """
    exception_data: Sequence = exception.errors()
    parametr_type = exception_data[0].get("loc")[0]
    field = exception_data[0].get("loc")[1]
    message = exception_data[0].get("msg")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": {
                    "parametr_type": parametr_type,
                    "field": field,
                    "message": message,
                }
            }
        ),
    )
