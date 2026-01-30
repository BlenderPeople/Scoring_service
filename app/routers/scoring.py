from fastapi import APIRouter, status

from app.schemas import ScoreResponse, ScoreRequest

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

def get_credit(request: ScoreRequest) -> ScoreResponse:
    """Получить кредит по client_id."""
    income = request.income
    history = request.history
    if history != []:
        return ScoreResponse(
            result = "30000"
        )
    if income > 50000 and history == []:
        return ScoreResponse(
            result = "20000"
            )
    
    if 30000 < income <= 50000 and history == []:
        return ScoreResponse(
            result = "10000"
        )
    else: 
        return ScoreResponse(
            result = "0"
        )