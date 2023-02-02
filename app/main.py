from fastapi import FastAPI

# from db_session import engine
from db_session import connect_db

# from db_base import Base


# def create_tables():
#     print("create tables")
#     Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(
        title="The mini blog",
        version="0.0.1",
        description="The test case",
    )
    # create_tables()
    connect_db()
    return app


app = start_application()
