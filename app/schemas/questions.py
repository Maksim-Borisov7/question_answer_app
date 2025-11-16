from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from app.schemas.answers import AnswerResponse


class QuestionSchemas(BaseModel):
    text: str


class QuestionAllResponse(BaseModel):
    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionIDResponse(QuestionAllResponse):
    answers: List[AnswerResponse]


