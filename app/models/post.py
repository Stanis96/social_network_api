from datetime import datetime

import sqlalchemy

from sqlalchemy.orm import relationship

from app.db.db_session import Base


reaction_like = sqlalchemy.Table(
    "reaction_likes",
    Base.metadata,
    sqlalchemy.Column(
        "post_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sqlalchemy.Column(
        "user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), primary_key=True
    ),
)

reaction_dislike = sqlalchemy.Table(
    "reaction_dislikes",
    Base.metadata,
    sqlalchemy.Column(
        "post_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Post(Base):
    __tablename__ = "posts"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    date_creation = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now())
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    likes = relationship(
        "User", secondary=reaction_like, backref="likes", lazy="joined", single_parent=True
    )
    dislikes = relationship(
        "User", secondary=reaction_dislike, backref="dislikes", lazy="joined", single_parent=True
    )

    def count_likes(self) -> int:
        return len(self.likes)

    def count_dislikes(self) -> int:
        return len(self.dislikes)
