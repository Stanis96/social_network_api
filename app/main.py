from fastapi import FastAPI

from app.db.base_class import Base
from app.db.db_session import engine


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(
        title="The mini blog",
        version="0.0.1",
        description="The test case",
    )
    # include_router(app)
    create_tables()
    return app


app = start_application()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
