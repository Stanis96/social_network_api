from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generic

from app.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def connect_db():
    try:
        engine.connect()
    except Exception as e:
        print(f"Database conn error: {e}")
    print(f"Connection {engine.url}")


def get_session() -> Generic:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
