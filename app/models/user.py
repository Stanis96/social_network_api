import sqlalchemy

from sqlalchemy.orm import relationship

from app.db.db_session import Base


class User(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    posts = relationship("Post", backref="posts", cascade="all", lazy="joined")
