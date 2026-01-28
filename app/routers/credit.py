from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import UserCreate, UserResponse, UserUpdate
from app.dependencies import get_db, Database

router = APIRouter(
    prefix="/credit",
    tags=["credit"],
    responses={404: {"description": "Credit not found"}}
)

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую кредитную историю",
    description="Создает новую кредитную историю в базе данных"
)

def create_credit(credit: CreditModel, db: Database = Depends(get_db)) -> UserResponse:
    """
    Создать новую кредитную историю.

    - **client_id**: уникальный идентификатор клиента
    - **income**: доход клиента
    - **history**: история кредитов клиента
        - **sum**: сумма кредита
        - **date**: дата выдачи кредита
        - **status**: статус кредита
    """
    if db.credit_exists(credit.client_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credit history already exists"
        )
    new_credit = db.create_credit(id=credit.client_id, income=credit.income, history=credit.history)

    return UserResponse(
        client_id=new_credit.id,
        income=new_credit.income,
        history=new_credit.history
        )

@router.get(
    "/{client_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить кредитную историю по client_id",
    description="Возвращает кредитную историю для заданного client_id"
    )
def get_credit(client_id: int, db: Database = Depends(get_db)) -> UserResponse:
    """Получить кредитную историю по client_id."""
    credit = db.get_credit_by_client_id(client_id)
    if not credit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Кредитная история не найдена"
        )
    return UserResponse(
        client_id=credit.id,
        income=credit.income,
        history=credit.history
        )

@router.patch(
    "/{client_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить кредитную историю по client_id",
    description="Обновляет кредитную историю для заданного client_id"
    )

def update_credit(
    client_id: int,
    credit_update: UserUpdate,
    db: Database = Depends(get_db)
    ) -> UserResponse:
    """Обновить кредитную историю по client_id."""
    credit = db.get_credit_by_client_id(client_id)
    if not credit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Кредитная история не найдена"
        )
    updated_credit = db.update_credit(
        client_id,
        income=credit_update.income,
        history=credit_update.history
        )
    return UserResponse(
        client_id=updated_credit.id,
        income=updated_credit.income,
        history=updated_credit.history
        )

@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить кредитную историю по client_id",
    description="Удаляет кредитную историю для заданного client_id"
    )

def delete_credit(client_id: int, db: Database = Depends(get_db)):
    """Удалить кредитную историю по client_id."""
    credit = db.get_credit_by_client_id(client_id)
    if not credit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Кредитная история не найдена"
        )
    db.delete_credit(client_id)
    return None

