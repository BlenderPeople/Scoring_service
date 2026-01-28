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

    def close(self):
        """Закрыть подключение к базе."""
        self._connected = False
        logger.info("Database connection closed")

    def create_credit(self, id: int, income: float, history: list[dict]) -> CreditModel:
        """Создать новую кредитную историю."""
        credit = CreditModel(client_id=id, income=income, credit_history=history)
        self.credits[id] = credit
        logger.info(f"Создана кредитная история для client_id={id}")
        return credit

    def get_credit_by_client_id(self, client_id: int) -> Optional[CreditModel]:
        """Получить кредитную историю по client_id."""
        return self.credits.get(client_id)

    def credit_exists(self, client_id: int) -> bool:
        """Проверить, существует ли кредитная история для client_id."""
        return client_id in self.credits
    
    def update_credit(self, client_id: int, income: Optional[float] = None, history: Optional[list[dict]] = None) -> Optional[CreditModel]:
        """Обновить кредитную историю по client_id."""
        credit = self.credits.get(client_id)
        if not credit:
            return None
        if income is not None:
            credit.income = income
        if history is not None:
            credit.credit_history = history
        logger.info(f"Обновлена кредитная история для client_id={client_id}")
        return credit
    
    def delete_credit(self, client_id: int) -> None:
        """Удалить кредитную историю по client_id."""
        if client_id in self.credits:
            del self.credits[client_id]
            logger.info(f"Удалена кредитная история для client_id={client_id}")

_db_instance: Optional[Database] = None

def get_db() -> Generator[Database, None, None]:
    """Получить экземпляр базы данных."""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
        logger.info("Создан новый экземпляр базы данных")
    try:
        yield _db_instance
    finally:
        _db_instance.close()