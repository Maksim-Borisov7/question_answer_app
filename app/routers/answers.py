from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.models import AnswerModels
from app.schemas.answers import AnswerSchemas, AnswerResponse
from app.database.database import database
from app.use_cases.answers.create_answer import CreateAnswerUseCase
from app.use_cases.answers.get_answer import GetAnswerUseCase
from app.use_cases.answers.delete_answer import DeleteAnswerUseCase

router = APIRouter(tags=["Answers"])


@router.post(
    '/questions/{id}/answers/',
    summary='добавить ответ к вопросу',
    )
async def add_answer(id: int,
                     data: Annotated[AnswerSchemas, Depends()],
                     session: AsyncSession = Depends(database.get_session)
                     ) -> dict:
    return await CreateAnswerUseCase.execute(id, data, session)


@router.get(
    '/answers/{id}',
    summary='получить конкретный ответ',
    response_model=AnswerResponse
    )
async def get_answer(id: int,
                     session: AsyncSession = Depends(database.get_session)
                     ) -> AnswerModels:
    return await GetAnswerUseCase.execute(id, session)


@router.delete(
    '/answers/{id}',
    summary='удалить ответ',
    status_code=status.HTTP_200_OK
    )
async def delete_answer(id: int,
                        session: AsyncSession = Depends(database.get_session)
                        ) -> dict:
    return await DeleteAnswerUseCase.execute(id, session)
