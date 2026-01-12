import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import healthcheck_router, notify_router
from app.core.settings import settings as s
from app.logs.logging_setup import setup_logging
from app.logs.middleware_logging_setup import logging_middleware

routers = [notify_router, healthcheck_router]
is_prod = s.env == "prod"

setup_logging()


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Приложение запущено")
    yield


app = FastAPI(
    title=s.fastapi.title,
    version=s.fastapi.version,
    lifespan=lifespan,
    docs_url=s.fastapi.docs,
    redoc_url=s.fastapi.redoc,
    openapi_url=s.fastapi.openapi,
)

app.middleware("http")(logging_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=s.cors.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in routers:
    app.include_router(route)


if __name__ == "__main__":
    uvicorn.run("main:app", host=s.host, port=s.port)
