import uuid

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import AnswerModels, QuestionModels
from app.logs.logger import logger
from app.repositories.questions import QuestionRepository
from app.schemas.answers import AnswerSchemas


class AnswerRepository:
    """
    Репозиторий для работы с сущностью Answer в базе данных.

    Предоставляет методы для добавления, получения и удаления ответов к вопросам.

    Методы:
        - create_answer(question_id: int, text: str, user_id: uuid.UUID, session: AsyncSession) -> AnswerModels
        - get_answer_by_id(answer_id, session) -> AnswerModels
        - delete_answer_by_id(answer_id, session) -> dict
    """

    model = AnswerModels

    @classmethod
    async def create_answer(
        cls,
        question_id: int,
        text: str,
        user_id: uuid.UUID,
        session: AsyncSession
    ) -> AnswerModels:
        """
        Добавляет ответ для указанного вопроса.

        Args:
            question_id (int): ID вопроса, к которому создаётся ответ.
            text (str): Данные нового ответа(id, text, user_id).
            user_id (uuid.UUID): генерируется рандомный UUID пользователя
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            AnswerModels: Созданный объект ответа с ID.
        """
        answer = cls.model(
            question_id=question_id,
            text=text,
            user_id=user_id
        )
        session.add(answer)
        await session.commit()
        return answer

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
        """
        query = select(cls.model).where(cls.model.id == answer_id)
        result = await session.execute(query)
        answer = result.scalar_one_or_none()
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
        """
        await session.execute(delete(cls.model).where(cls.model.id == answer_id))
        await session.commit()
        return {"message": f"Ответ {answer_id} удалён"}

