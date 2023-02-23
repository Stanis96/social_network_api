import os
import sys

from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings
from pydantic import PostgresDsn


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)


class Settings(BaseSettings):
    PROJECT_TITLE: Optional[str]
    PROJECT_VERSION: Optional[str]
    PROJECT_DESCRIPTION: Optional[str]

    SECRET_KEY: Optional[str]
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_USER: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_SERVER: Optional[str]
    POSTGRES_PORT: Optional[str]
    POSTGRES_DB: Optional[str]

    DATABASE_URL: Optional[PostgresDsn]

    TEST_POSTGRES_USER: Optional[str]
    TEST_POSTGRES_PASSWORD: Optional[str]
    TEST_POSTGRES_SERVER: Optional[str]
    TEST_POSTGRES_PORT: Optional[str]
    TEST_POSTGRES_DB: Optional[str]

    TEST_DATABASE_URL: Optional[PostgresDsn]

    TEST_USER_EMAIL: str = "testuser@example.com"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings(_env_file=".env")
