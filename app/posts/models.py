import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Post(Base):
    __tablename__ = "post"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    date_creation = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now())
    user_id = sqlalchemy.Column(sqlalchemy.ForeignKey("user.id"), nullable=False)
    likes = relationship("Like", back_populates="like")
    dislikes = relationship("Dislike", back_populates="dislike")

    def likes_count(self) -> int:
        return len(self.likes)

    def dislikes_count(self) -> int:
        return len(self.dislikes)


class Like(Base):
    __tablename__ = "like"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.ForeignKey("user.id"), nullable=False)
    like = relationship("Post", back_populates="likes")


class Dislike(Base):
    __tablename__ = "dislike"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.ForeignKey("user.id"), nullable=False)
    dislike = relationship("Post", back_populates="dislikes")
