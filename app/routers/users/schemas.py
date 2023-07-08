from fastapi import Body, Query
from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    username: str = Body(max_length=30, min_length=3)
    email: EmailStr
    age: int = Body(le=150, ge=14)
    location: str = Body(default="Stavropol", max_length=30, min_length=3)


class UserCreate(BaseModel):
    username: str = Body(max_length=30, min_length=3)
    email: EmailStr
    password: str = Body(max_length=30, min_length=6)
    age: int = Body(le=150, ge=14)
    location: str = Body(default="Stavropol", max_length=30, min_length=3)

    class Config:
        orm_mode = True


class UserFilter(BaseModel):
    age: int | None = Query()
    location: str | None = Query()


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    age: int | None = None
    location: str | None = None
