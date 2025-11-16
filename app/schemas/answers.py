from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnswerSchemas(BaseModel):
    text: str
    user_id: Optional[UUID] = None


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    user_id: UUID
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


