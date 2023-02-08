from datetime import datetime

import sqlalchemy

from sqlalchemy.orm import relationship

from app.db.db_session import Base


class Post(Base):
    __tablename__ = "posts"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    date_creation = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now())
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False
    )
    owner = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="likes")
    dislikes = relationship("Dislike", back_populates="dislikes")

    def likes_count(self) -> int:
        return len(self.likes)

    def dislikes_count(self) -> int:
        return len(self.dislikes)


class Like(Base):
    __tablename__ = "likes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False
    )
    post_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"), nullable=False
    )
    likes = relationship("Post", back_populates="likes")


class Dislike(Base):
    __tablename__ = "dislikes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False
    )
    post_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"), nullable=False
    )
    dislikes = relationship("Post", back_populates="dislikes")
