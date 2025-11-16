import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_get_all_questions_structure():
    """
        Проверяет эндпоинт GET /questions/.

        Логика теста:
        - Отправляется GET-запрос к /questions/.
        - Проверяется, что статус ответа 200.
        - Проверяется, что ответ является списком.
        - Для каждого вопроса проверяются обязательные поля: id, text, created_at.
    """
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        response = await client.get("/questions/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for question in data:
        assert "id" in question
        assert "text" in question
        assert "created_at" in question

