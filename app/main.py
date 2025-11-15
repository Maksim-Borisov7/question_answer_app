from contextlib import asynccontextmanager
from app.logs.logger import logger
from fastapi import FastAPI
from app.database.db_helper import db_helper
from app.routes.questions import router as router_questions
from app.routes.answer import router as router_answer


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Запуск сервера")
        await db_helper.delete_table()
        await db_helper.create_table()
        logger.info("База готова к работе")
        yield
        logger.info("Выключение")
    except ConnectionRefusedError as e:
        logger.warning(f"Не удалось подключиться к БД: {e}")

app = FastAPI(lifespan=lifespan)
app.include_router(router_questions)
app.include_router(router_answer)
