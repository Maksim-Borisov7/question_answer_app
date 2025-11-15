from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.database.models import QuestionModels
from app.logs.logger import logger
from app.repositories.questions.schemas import QuestionSchemas


class QuestionRepository:
    model = QuestionModels
    """Репозиторий для работы с сущностью Question в базе данных.

    Методы:
    - all_questions(session: AsyncSession) -> list[QuestionModels]
    - add_question(data: QuestionSchemas, session: AsyncSession) -> dict
    - get_question_by_id(id: int, session: AsyncSession) -> QuestionModels
    - delete_question_by_id(id: int, session: AsyncSession) -> dict
    """
    @classmethod
    async def all_questions(cls, session: AsyncSession) -> list[QuestionModels]:
        """Получение списка всех вопросов"""
        try:
            query = select(cls.model)
            result = await session.execute(query)
            questions = result.scalars().all()
            logger.info("Список вопросов получен")
            return list(questions)
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении всех вопросов: {e}")
            raise HTTPException(status_code=500, detail="Ошибка сервера")

    @classmethod
    async def add_question(cls, data: QuestionSchemas, session: AsyncSession) -> dict:
        """Создать новый вопрос"""
        try:
            data_dict = data.model_dump()
            question = cls.model(**data_dict)
            session.add(question)
            await session.commit()
            logger.info(f"Создан вопрос с ID {question.id}")
            return {'message': "Вопрос создан"}
        except Exception as e:
            logger.error(f"Ошибка при создании вопроса: {e}")
            raise

    @classmethod
    async def get_question_by_id(cls, id: int, session: AsyncSession) -> QuestionModels:
        """Получить вопрос по ID"""
        try:
            query = (select(cls.model).where(cls.model.id == id).options
                     (selectinload(cls.model.answers)))
            result = await session.execute(query)
            question = result.scalar_one_or_none()
            if question is None:
                raise HTTPException(status_code=404, detail="Вопрос не найден")
            logger.info(f"Получен вопрос с ID {id}")
            return question
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении вопроса {id}: {e}")
            raise HTTPException(status_code=500, detail="Ошибка сервера")

    @classmethod
    async def delete_question_by_id(cls, id: int, session: AsyncSession) -> dict:
        """Удалить вопрос по ID"""
        try:
            await cls.get_question_by_id(id, session)
            await session.execute(delete(cls.model).where(cls.model.id == id))
            await session.commit()
            logger.info(f"Удален вопрос с ID {id} вместе с ответами")
            return {"message": "Вопрос успешно удален вместе с ответами"}
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении вопроса {id}: {e}")
            raise HTTPException(status_code=500, detail="Не удалось удалить вопрос")


