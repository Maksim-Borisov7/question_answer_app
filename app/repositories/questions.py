from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.database.models import QuestionModels
from app.logs.logger import logger
from app.schemas.questions import QuestionSchemas


class QuestionRepository:
    """
    Репозиторий для работы с сущностью Question в базе данных.

    Методы:
    - all_questions(session: AsyncSession) -> list[QuestionModels]
    - add_question(data: dict, session: AsyncSession) -> QuestionModels
    - get_question_by_id(id: int, session: AsyncSession) -> QuestionModels
    - delete_question_by_id(id: int, session: AsyncSession)
    """

    model = QuestionModels

    @classmethod
    async def all_questions(cls, session: AsyncSession) -> list[QuestionModels]:
        """
        Получает список всех вопросов из базы данных.

        session: Активная асинхронная сессия SQLAlchemy.
        return: Список объектов `QuestionModels`.
        """
        query = select(cls.model)
        result = await session.execute(query)
        questions = result.scalars().all()
        return list(questions)

    @classmethod
    async def add_question(cls, data: dict, session: AsyncSession) -> QuestionModels:
        """
        Создаёт новый вопрос в базе данных.

        data: Данные вопроса
        session: Активная асинхронная сессия SQLAlchemy.
        return: Созданный объект `QuestionModels`.
        """
        question = cls.model(**data)
        session.add(question)
        await session.commit()
        return question

    @classmethod
    async def get_question_by_id(cls, id: int, session: AsyncSession) -> QuestionModels:
        """
        Получает вопрос по его идентификатору, включая связанные ответы.

        id: ID вопроса.
        session: Активная асинхронная сессия SQLAlchemy.
        return: Объект `QuestionModels` или None, если вопрос не найден.
       """
        query = (select(cls.model).where(cls.model.id == id).options
                 (selectinload(cls.model.answers)))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def delete_question_by_id(cls, id: int, session: AsyncSession):
        """
        Удаляет вопрос по его ID.
        id: ID удаляемого вопроса.
        session: Активная асинхронная сессия SQLAlchemy.
        """
        await session.execute(delete(cls.model).where(cls.model.id == id))
        await session.commit()



