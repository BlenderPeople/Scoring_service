from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import UserCreate, UserResponse, UserUpdate
from app.dependencies import get_db, Database

router = APIRouter(
    prefix="/credit",
    tags=["credit"]
    responses={404: {"description": "Credit not found"}}
)

@router.post(
    "/"
    response_model=UserResponse
    status_code=status.HTTP_201_CREATED
    summary="Создать новую кредитную запись"
    description="Создает новую запись кредита в базе данных"
)

def create_credit(