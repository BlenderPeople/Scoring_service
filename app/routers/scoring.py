from fastapi import APIRouter, Depends, status
import redis.asyncio as redis
from app.schemas import ScoreResponse, ScoreRequest
from app.dependencies import get_redis

def make_key(request: ScoreRequest) -> str:
    history_flag = "non_empty" if request.history else "empty"
    return f"score:{request.income}:{history_flag}"

async def cached_response(key: str, approved: float, redis_client: redis.Redis) -> ScoreResponse:
    cached = await redis_client.get(key)
    if cached is not None:
        return ScoreResponse(result=float(cached))
    await redis_client.set(key, approved, ex=300)
    return ScoreResponse(result=approved)

router = APIRouter(
    tags=["Scoring"],
    responses={404: {"description": "Не найдено"}},
)


@router.post(
    "",
    response_model=ScoreResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Проверить возможность выдачи кредита",
    description="Проверяет возможность выдачи кредита на основе дохода и кредитной истории клиента"
)
async def get_credit(
    request: ScoreRequest,
    redis_client: redis.Redis = Depends(get_redis),
) -> ScoreResponse:
    """Получить кредит по client_id."""
    key = make_key(request)
    if request.history:
        return await cached_response(key, 30000.0, redis_client)
    if request.income > 50000:
        return await cached_response(key, 20000.0, redis_client)
    if request.income > 30000:
        return await cached_response(key, 10000.0, redis_client)
    return await cached_response(key, 0.0, redis_client)