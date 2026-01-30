import logging

from fastapi import FastAPI

from app.config import get_settings
from app.routers import score_router

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.info(
    f"Starting {settings.app_name} v{settings.app_version} on {settings.host}:{settings.port}"
)

app = FastAPI(
    title=settings.app_name,
    description="""
## Сервис скоринга

### Возможности
- Подбор суммы кредита на основе дохода и кредитной истории клиента.
    """,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(score_router, prefix="/score")

@app.get("/", tags=["root"])
def root():
    return {
        "message": "Добро пожаловать в Scoring Service API!",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }

