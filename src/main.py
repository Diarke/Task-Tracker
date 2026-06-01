from fastapi import FastAPI
import uvicorn

from src.core.config import settings


app = FastAPI(
    debug=settings.APP.DEBUG,
    title=settings.APP.TITLE,
    summary=settings.APP.SUMMARY,
    description=settings.APP.DESCRIPTION,
    version=settings.APP.VERSION,
    docs_url=settings.APP.DOCS_URL,
    redoc_url=settings.APP.REDOC_URL,
)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
