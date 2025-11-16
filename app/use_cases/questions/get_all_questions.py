from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import QuestionModels
from app.logs.logger import logger
from app.repositories.questions import QuestionRepository


class GetAllQuestionsUseCase:
    """
      Use case для получения списка всех вопросов.

      Логика:
      - Загружает список вопросов через репозиторий.
      - Возвращает модели вопросов.
    """
    @staticmethod
    async def execute(session: AsyncSession) -> list[QuestionModels]:
        res = await QuestionRepository.all_questions(session)
        logger.info("Список вопросов получен")
        return res
