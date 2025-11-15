from contextlib import asynccontextmanager
from app.logs.logger import logger
from fastapi import FastAPI
from app.routes.questions import router as router_questions
from app.routes.answer import router as router_answer


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Запуск сервера")
        yield
        logger.info("Выключение")
    except ConnectionRefusedError as e:
        logger.warning(f"Не удалось подключиться к БД: {e}")

app = FastAPI(lifespan=lifespan)
app.include_router(router_questions)
app.include_router(router_answer)
