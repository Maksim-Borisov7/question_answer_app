from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.answers import AnswerRepository


class DeleteAnswerUseCase:
    """
    Use case для удаления ответа.

    Логика:
    - Проверяет существование ответа.
    - Выполняет удаление ответа через репозиторий.
    - Возвращает сообщение об успешном удалении.
    """
    @staticmethod
    async def execute(answer_id: int, session: AsyncSession) -> dict:
        answer = await AnswerRepository.get_answer_by_id(answer_id, session)
        if answer is None:
            raise HTTPException(status_code=404, detail="Ответ не найден")
        await AnswerRepository.delete_answer_by_id(answer_id, session)
        return {"message": f"Ответ {answer_id} удалён"}
