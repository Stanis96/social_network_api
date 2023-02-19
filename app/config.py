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
    ALGORITHM: Optional[str] = os.getenv("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: Optional[str] = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: Optional[str] = os.getenv("POSTGRES_PORT", default="5432")
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")

    TEST_POSTGRES_USER: Optional[str] = os.getenv("TEST_POSTGRES_USER", default="postgres")
    TEST_POSTGRES_PASSWORD: Optional[str] = os.getenv("TEST_POSTGRES_PASSWORD", default="postgres")
    TEST_POSTGRES_SERVER: Optional[str] = os.getenv("TEST_POSTGRES_SERVER", default="localhost")
    TEST_POSTGRES_PORT: Optional[str] = os.getenv("TEST_POSTGRES_PORT", default="5433")
    TEST_POSTGRES_DB: Optional[str] = os.getenv("TEST_POSTGRES_DB", default="postgres")

    TEST_DATABASE_URL = (
        f"postgresql+psycopg2://{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}@"
        f"{TEST_POSTGRES_SERVER}:{TEST_POSTGRES_PORT}/{TEST_POSTGRES_DB}"
    )
    DATABASE_URL = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:"
        f"{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    TEST_USER_EMAIL: str = "testuser@example.com"


settings = Settings()
