from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def connect_db():
    try:
        engine.connect()
    except Exception as err:
        print(f"Database conn error: {err}")
    print(f"Connection {engine.url}")


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
