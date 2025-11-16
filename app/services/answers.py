


class AnswerService:
    @staticmethod
    async def create_answer(question_id: int, data: AnswerSchemas, session: AsyncSession):
        # 1. Проверка существования вопроса
        question = await AnswerRepository.get_question(session, question_id)
        if not question:
            raise HTTPException(404, "Вопрос не найден")

        # 2. Генерация UUID
        user_id = data.user_id or uuid.uuid4()

        # 3. Создание ответа
        answer = await AnswerRepository.create(
            session,
            data={"question_id": question_id, "text": data.text, "user_id": user_id}
        )

        # 4. Commit
        await session.commit()

        return {"message": "Ответ добавлен", "id": answer.id}