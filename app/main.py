import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.routers import health, ranking, refeicoes
from app.storage import storage

settings = get_settings()
logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger("ru-ometro")


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.seed_data:
        storage.seed()
        logger.info("Seed data loaded")
    logger.info("%s version %s started", settings.app_name, settings.app_version)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API para avaliar as refeicoes do RU.",
    lifespan=lifespan,
)
app.include_router(health.router)
app.include_router(refeicoes.router)
app.include_router(ranking.router)
