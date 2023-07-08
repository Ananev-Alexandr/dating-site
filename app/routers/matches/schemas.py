from datetime import date

from pydantic import BaseModel


class MatchCreate(BaseModel):
    user1_id: int
    user2_id: int


class MatchResponse(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    match_date: date
