from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from app.config import settings
from app.database.models import Base
from app.main import logger


class Database:
    """Класс для управления подключением и сессиями базы данных."""
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncSession:
        """Возвращает асинхронную сессию базы данных."""
        try:
            async with self.session_factory() as session:
                logger.debug("Создана новая асинхронная сессия базы данных.")
                yield session
        except Exception as e:
            logger.exception(f"Ошибка при создании сессии: {e}")
            raise

    async def create_table(self):
        """Создаёт все таблицы, описанные в models.Base."""
        logger.info("Создание таблиц в базе данных...")
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Таблицы успешно созданы.")
        except Exception as e:
            logger.exception(f"Ошибка при создании таблиц: {e}")
            raise

    async def delete_table(self):
        """Удаляет все таблицы."""
        logger.warning("Удаление всех таблиц из базы данных...")
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            logger.warning("Все таблицы удалены.")
        except Exception as e:
            logger.exception(f"Ошибка при удалении таблиц: {e}")
            raise


db_helper = Database(
    url=settings.PG_URL,
    echo=settings.echo,
)
