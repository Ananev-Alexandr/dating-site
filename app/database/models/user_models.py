from sqlalchemy import Column, Integer, String

from app.database.db import Base


class User(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    age = Column(Integer)
    location = Column(String)
