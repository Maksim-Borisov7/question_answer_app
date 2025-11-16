from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.questions import QuestionRepository
from app.schemas.questions import QuestionSchemas


class CreateQuestionUseCase:
    """
        Use case для создания нового вопроса.

        Логика:
        - Принимает данные нового вопроса.
        - Передаёт их репозиторию для сохранения.
        - Возвращает результат создания в удобном формате.
    """
    @staticmethod
    async def execute(data: QuestionSchemas, session: AsyncSession) -> dict:
        data_dict = data.model_dump()
        question = await QuestionRepository.add_question(data_dict, session)
        return {"message": "Вопрос создан", "id": question.id}

