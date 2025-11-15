from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Base(DeclarativeBase):
    pass


class QuestionModels(Base):
    """
    Модель вопроса.

    Attributes:
        id: Уникальный ID вопроса.
        text: Текст вопроса.
        created_at: Дата создания.
        answers: Связанные ответы.
    """
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    answers: Mapped[list["AnswerModels"]] = relationship("AnswerModels",
                                                         back_populates='question',
                                                         cascade="all"
                                                         )


class AnswerModels(Base):
    """
    Модель ответа на вопрос.

    Attributes:
        id: Уникальный ID ответа.
        question_id: Ссылка на QuestionModels
        user_id: UUID пользователя
        text: Текст ответа.
        created_at: Дата создания.
        question: Связанные ответы.
        """
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False
    )
    text: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    question: Mapped["QuestionModels"] = relationship("QuestionModels", back_populates="answers")
