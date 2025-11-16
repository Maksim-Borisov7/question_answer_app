import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.logs.logger import logger
from app.repositories.answers import AnswerRepository
from app.repositories.questions import QuestionRepository
from app.schemas.answers import AnswerSchemas


class CreateAnswerUseCase:
    """
       Use case для создания ответа на вопрос.

       Логика:
       - Проверяет существование вопроса.
       - Генерирует UUID пользователя, если он не передан.
       - Создаёт ответ через репозиторий.
       - Возвращает словарь с результатом создания
    """

    @staticmethod
    async def execute(question_id: int, data: AnswerSchemas, session: AsyncSession) -> dict:
        question = await QuestionRepository.get_question_by_id(question_id, session)
        if question is None:
            logger.warning(f"Попытка добавить ответ к несуществующему вопросу ID {question_id}")
            raise HTTPException(status_code=404, detail="Вопрос не найден")

        user_id = data.user_id or str(uuid.uuid4())
        answer = await AnswerRepository.create_answer(
            question_id=question_id,
            text=data.text,
            user_id=user_id,
            session=session
        )
        logger.info(f"Создан ответ с ID {answer.id} для вопроса {question_id}")
        return {"message": "Ответ добавлен", "id": answer.id}

