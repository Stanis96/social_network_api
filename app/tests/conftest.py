from typing import Any
from typing import Generator

import pytest

from fastapi import Depends
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db.db_base import Base
from app.db.db_session import get_session
from app.routers.base import router_api
from app.routers.utils.user_utils import UserService
from app.tests.utils import authentication_token


engine = create_engine(settings.TEST_DATABASE_URL)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def start_application():
    app = FastAPI()
    app.include_router(router_api)
    return app


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    def _get_session():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = _get_session
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def normal_user_token(client: TestClient, user_tools: UserService = Depends()):
    return authentication_token(
        client=client, email=settings.TEST_USER_EMAIL, user_tools=user_tools
    )
