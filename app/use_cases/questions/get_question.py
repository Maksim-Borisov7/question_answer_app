from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import QuestionModels
from app.logs.logger import logger
from app.repositories.questions import QuestionRepository


class GetQuestionUseCase:
    """
      Use case для получения конкретного вопроса по его ID.

      Логика:
      - Загружает вопрос через репозиторий.
      - Проверяет его существование.
      - Возвращает модель вопроса.
    """
    @staticmethod
    async def execute(id: int, session: AsyncSession) -> QuestionModels:
        question = await QuestionRepository.get_question_by_id(id, session)
        if question is None:
            raise HTTPException(status_code=404, detail="Вопрос не найден")
        logger.info(f"Получен вопрос с ID {id}")
        return question

