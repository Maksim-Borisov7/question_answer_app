from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from app.config import settings
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


database = Database(
    url=settings.PG_URL,
    echo=settings.echo,
)
