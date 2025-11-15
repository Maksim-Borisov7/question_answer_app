import uuid

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import AnswerModels, QuestionModels
from app.logs.logger import logger
from app.repositories.questions.crud import QuestionRepository
from app.repositories.answer.schemas import AnswerSchemas


class AnswerRepository:
    """
    Репозиторий для работы с сущностью Answer в базе данных.

    Предоставляет методы для добавления, получения и удаления ответов к вопросам.

    Методы:
        - addition_answer(question_id, data, session) -> dict
        - get_answer_by_id(answer_id, session) -> AnswerModels
        - delete_answer_by_id(answer_id, session) -> dict
    """

    model = AnswerModels

    @classmethod
    async def addition_answer(
        cls,
        question_id: int,
        data: AnswerSchemas,
        session: AsyncSession
    ) -> dict:
        """
        Добавляет ответ для указанного вопроса.

        Args:
            question_id (int): ID вопроса, к которому создаётся ответ.
            data (AnswerSchemas): Данные нового ответа.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            AnswerModels: Созданный объект ответа с ID.

        Raises:
            HTTPException: Если вопрос с указанным ID не найден.
        """
        question = await cls._get_question_by_id(question_id, session)
        if question is None:
            logger.warning(f"Попытка добавить ответ к несуществующему вопросу ID {question_id}")
            raise HTTPException(status_code=404, detail="Вопрос не найден")

        answer = cls.model(
            question_id=question_id,
            text=data.text,
            user_id=data.user_id or uuid.uuid4()
        )
        session.add(answer)
        try:
            await session.commit()
            logger.info(f"Создан ответ с ID {answer.id} для вопроса {question_id}")
            return {"message": "Ответ добавлен", "id": answer.id}
        except Exception as e:
            logger.error(f"Ошибка при добавлении ответа к вопросу {question_id}: {e}")
            raise HTTPException(status_code=500, detail="Не удалось добавить ответ")

    @classmethod
    async def get_answer_by_id(
        cls,
        answer_id: int,
        session: AsyncSession
    ) -> AnswerModels:
        """
        Получает ответ по его ID.

        Args:
            answer_id (int): ID ответа.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            AnswerModels: Объект ответа.

        Raises:
            HTTPException: Если ответ не найден.
        """
        query = select(cls.model).where(cls.model.id == answer_id)
        result = await session.execute(query)
        answer = result.scalar_one_or_none()
        if answer is None:
            logger.warning(f"Ответ с ID {answer_id} не найден")
            raise HTTPException(status_code=404, detail="Ответ не найден")
        logger.info(f"Получен ответ с ID {answer_id}")
        return answer

    @classmethod
    async def delete_answer_by_id(
        cls,
        answer_id: int,
        session: AsyncSession
    ) -> dict:
        """
        Удаляет ответ по ID.

        Args:
            answer_id (int): ID ответа.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            dict: Сообщение об успешном удалении.

        Raises:
            HTTPException: Если ответ не найден.
        """
        try:
            await cls.get_answer_by_id(answer_id, session)
            await session.execute(delete(cls.model).where(cls.model.id == answer_id))
            await session.commit()
            logger.info(f"Удалён ответ с ID {answer_id}")
            return {"message": f"Ответ {answer_id} удалён"}
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении ответа", e)
            raise HTTPException(status_code=500, detail="Ошибка сервера")

    @staticmethod
    async def _get_question_by_id(
        question_id: int,
        session: AsyncSession
    ) -> QuestionModels | None:
        """
        Вспомогательный метод для получения вопроса по ID.

        Args:
            question_id (int): ID вопроса.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            QuestionModels | None: Объект вопроса или None, если не найден.
        """
        query = select(QuestionRepository.model).where(QuestionRepository.model.id == question_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
