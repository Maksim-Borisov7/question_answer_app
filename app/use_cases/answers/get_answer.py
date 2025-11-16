from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import AnswerModels
from app.logs.logger import logger
from app.repositories.answers import AnswerRepository


class GetAnswerUseCase:
    """
     Use case для получения ответа по его ID.

     Логика:
     - Загружает ответ через репозиторий.
     - Проверяет факт существования.
     - Возвращает модель ответа.
     """
    @staticmethod
    async def execute(answer_id: int, session: AsyncSession) -> AnswerModels:
        answer = await AnswerRepository.get_answer_by_id(answer_id, session)
        if answer is None:
            logger.warning(f"Ответ с ID {answer_id} не найден")
            raise HTTPException(status_code=404, detail="Ответ не найден")
        return answer
