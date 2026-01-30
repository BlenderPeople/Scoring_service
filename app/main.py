import logging

from fastapi import FastAPI, Request, Response
from app.metrics import REQUEST_COUNTER, REQUEST_LATENCY
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
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

@app.get("/")
def root():
    return {
        "message": "Добро пожаловать в Scoring Service API!",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    status = str(response.status_code)
    REQUEST_COUNTER.labels(method=request.method, path=request.url.path, status=status).inc()
    REQUEST_LATENCY.labels(method=request.method, path=request.url.path, status=status).observe(duration)
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)