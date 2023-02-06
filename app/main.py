from fastapi import FastAPI

from app.config import settings
from app.db.db_session import connect_db
from app.routers.base import router_api


def include_router(app):
    app.include_router(router_api)


def start_application():
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
    )
    include_router(app)
    connect_db()
    return app


app = start_application()
