import sqlalchemy

from app.db_session import Base


class User(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
