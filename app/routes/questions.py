from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_helper import db_helper
from app.database.models import QuestionModels
from app.repositories.questions.crud import QuestionRepository
from app.repositories.questions.schemas import QuestionSchemas, QuestionIDResponse, QuestionAllResponse

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get(
    '/',
    summary='список всех вопросов',
    response_model=List[QuestionAllResponse]
)
async def get_all_questions(session: AsyncSession = Depends(db_helper.get_session)
                            ) -> list[QuestionModels]:
    return await QuestionRepository.all_questions(session)


@router.post(
    '/',
    summary='создать новый вопрос',
)
async def add_questions(question_data: Annotated[QuestionSchemas, Depends()],
                        session: AsyncSession = Depends(db_helper.get_session)
                        ) -> dict:
    return await QuestionRepository.add_question(question_data, session)


@router.get(
    '/{id}',
    summary='получить вопрос и все ответы на него',
    response_model=QuestionIDResponse
)
async def get_question(id: int,
                       session: AsyncSession = Depends(db_helper.get_session)
                       ) -> QuestionModels:
    return await QuestionRepository.get_question_by_id(id, session)


@router.delete(
    '/{id}',
    summary='удалить вопрос (вместе с ответами)',
    status_code=status.HTTP_200_OK
)
async def delete_question(id: int,
                          session: AsyncSession = Depends(db_helper.get_session)
                          ) -> dict:
    return await QuestionRepository.delete_question_by_id(id, session)
