from typing import List
from datetime import date

from pydantic import BaseModel, Field, field_validator

class HistoryEntry(BaseModel):
    """Модель записи кредитной истории."""

    sum: float = Field(..., description="Сумма кредита", example="10000.0")
    Date: date = Field(..., description="Дата записи", example="2023-01-15")
    is_closed: bool = Field(..., description="Статус кредита", example=True)

class ScoreRequest(BaseModel):
    """Ответ с информацией о возможной сумме кредита."""

    income: float = Field(..., description="Доход клиента", example=50000.0)
    history: List[HistoryEntry] = Field(
        default_factory=list,
        description="Список записей кредитной истории",
        example=[
            {"sum": "10000", "Date": "2023-01-15", "is_closed": True},
            {"sum": "5000", "Date": "2022-12-10", "is_closed": False},
        ],
    
    )

    @field_validator("income")
    def income_must_be_non_negative(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Доход не может быть отрицательным")
        return value
    
    @field_validator("history")
    def history_must_not_contain_negative_sums(cls, value: List[HistoryEntry]) -> List[HistoryEntry]:
        for entry in value:
            if float(entry.sum) < 0:
                raise ValueError("Сумма кредита в истории не может быть отрицательной")
        return value

class ScoreResponse(BaseModel):
    """Ответ с информацией о возможной сумме кредита."""
    result: float = Field(..., description="Результат скоринга")
