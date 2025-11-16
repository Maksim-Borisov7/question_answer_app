from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.database import database
from app.database.models import QuestionModels
from app.schemas.questions import QuestionSchemas, QuestionIDResponse, QuestionAllResponse
from app.use_cases.questions.get_question import GetQuestionUseCase
from app.use_cases.questions.get_all_questions import GetAllQuestionsUseCase
from app.use_cases.questions.add_questions import CreateQuestionUseCase
from app.use_cases.questions.delete_question import DeleteQuestionUseCase
router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get(
    '/',
    summary='список всех вопросов',
    response_model=List[QuestionAllResponse]
)
async def get_all_questions(session: AsyncSession = Depends(database.get_session)
                            ) -> list[QuestionModels]:
    return await GetAllQuestionsUseCase.execute(session)


@router.post(
    '/',
    summary='создать новый вопрос',
)
async def add_questions(question_data: Annotated[QuestionSchemas, Depends()],
                        session: AsyncSession = Depends(database.get_session)
                        ) -> dict:
    return await CreateQuestionUseCase.execute(question_data, session)


@router.get(
    '/{id}',
    summary='получить вопрос и все ответы на него',
    response_model=QuestionIDResponse
)
async def get_question(id: int,
                       session: AsyncSession = Depends(database.get_session)
                       ) -> QuestionModels:
    return await GetQuestionUseCase.execute(id, session)


@router.delete(
    '/{id}',
    summary='удалить вопрос (вместе с ответами)',
    status_code=status.HTTP_200_OK
)
async def delete_question(id: int,
                          session: AsyncSession = Depends(database.get_session)
                          ) -> dict:
    return await DeleteQuestionUseCase.execute(id, session)
