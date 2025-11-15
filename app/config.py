import os
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    HOST: str = os.getenv("HOST")
    USER: str = os.getenv("USER")
    PASSWORD: str = os.getenv("PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    PORT: str = os.getenv("PORT")
    PG_URL: str = os.getenv("PG_URL")
    BASE_DIR: ClassVar[Path] = Path(__file__).parent

    url: str = PG_URL
    echo: bool = False


settings = Settings()
