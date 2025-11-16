from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.questions import QuestionRepository


class DeleteQuestionUseCase:
    """
        Use case для удаления вопроса вместе с его ответами.

        Логика:
        - Проверяет существование вопроса.
        - Удаляет вопрос через репозиторий.
        - Возвращает сообщение об успешном удалении.
    """
    @staticmethod
    async def execute(id: int, session: AsyncSession) -> dict:
        question = await QuestionRepository.get_question_by_id(id, session)
        if question is None:
            raise HTTPException(status_code=404, detail="Вопрос не найден")
        await QuestionRepository.delete_question_by_id(id, session)
        return {"message": "Вопрос успешно удален вместе с ответами"}
