from datetime import date

from sqlalchemy import Column, Date, Identity, Integer

from app.database.db import Base


class Match(Base):
    __tablename__ = "match_table"

    id = Column(Integer, Identity(), primary_key=True, autoincrement=True)
    user1_id = Column(Integer, nullable=False)
    user2_id = Column(Integer, nullable=False)
    match_date = Column(Date, nullable=False, default=date.today())
