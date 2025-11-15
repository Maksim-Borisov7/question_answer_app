from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.models import AnswerModels
from app.repositories.answer.crud import AnswerRepository
from app.repositories.answer.schemas import AnswerSchemas, AnswerResponse
from app.database.db_helper import db_helper

router = APIRouter(tags=["Answers"])


@router.post(
    '/questions/{id}/answers/',
    summary='добавить ответ к вопросу',
    )
async def add_answer(id: int,
                     data: Annotated[AnswerSchemas, Depends()],
                     session: AsyncSession = Depends(db_helper.get_session)
                     ) -> dict:
    return await AnswerRepository.addition_answer(id, data, session)


@router.get(
    '/answers/{id}',
    summary='получить конкретный ответ',
    response_model=AnswerResponse
    )
async def get_answer(id: int,
                     session: AsyncSession = Depends(db_helper.get_session)
                     ) -> AnswerModels:
    return await AnswerRepository.get_answer_by_id(id, session)


@router.delete(
    '/answers/{id}',
    summary='удалить ответ',
    status_code=status.HTTP_200_OK
    )
async def delete_answer(id: int,
                        session: AsyncSession = Depends(db_helper.get_session)
                        ) -> dict:
    return await AnswerRepository.delete_answer_by_id(id, session)
