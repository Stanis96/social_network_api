import os
import sys

from typing import Optional

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)


class Settings:
    PROJECT_TITLE: Optional[str] = os.getenv("PROJECT_TITLE")
    PROJECT_VERSION: Optional[str] = os.getenv("PROJECT_VERSION")
    PROJECT_DESCRIPTION: Optional[str] = os.getenv("PROJECT_DESCRIPTION")

    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    ALGORITHM: Optional[str] = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: Optional[str] = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: Optional[str] = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")
    DATABASE_URL = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:"
        f"{POSTGRES_PORT}/{POSTGRES_DB}"
    )


settings = Settings()
