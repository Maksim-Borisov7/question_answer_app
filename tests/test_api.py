import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_get_all_questions():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test"
                           ) as ac:
        response = await ac.get('/questions/')
        print(response)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
