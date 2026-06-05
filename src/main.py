import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from src.core.config import settings
from src.db.session import check_db_connection
from src.api.routers import main_router


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db_connection()
    logger.info("Соединение с базой данных установлено")
    yield


app = FastAPI(
    lifespan=lifespan,
    debug=settings.APP.DEBUG,
    title=settings.APP.TITLE,
    summary=settings.APP.SUMMARY,
    description=settings.APP.DESCRIPTION,
    version=settings.APP.VERSION,
    docs_url=settings.APP.DOCS_URL,
    redoc_url=settings.APP.REDOC_URL,
)


app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
