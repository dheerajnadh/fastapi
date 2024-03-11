from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import null

from database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable =False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)