import logging
from datatime import datetime
from typing import Generator, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class CreditModel:
    """Модель кредитной истории клиента."""
    client_id: int
    income: float
    credit_history: list[dict] = field(default_factory=list)

class Database:
    """Имитация базы данных для хранения кредитных историй."""
    def __init__(self):
        self.credits = {}

    def create_credit(self, id: int, income: float, history: list[dict]) -> CreditModel:
        credit = CreditModel(client_id=id, income=income, credit_history=history)
        self.credits[id] = credit
        logger.info(f"Создана кредитная история для client_id={id}")
        return credit

    def get_credit_by_client_id(self, client_id: int) -> Optional[CreditModel]:
        return self.credits.get(client_id)

    def credit_exists(self, client_id: int) -> bool:
        return client_id in self.credits