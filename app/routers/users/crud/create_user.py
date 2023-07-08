from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.models import user_models
from app.helpers.password import get_password_hash
from app.routers.users.schemas import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = user_models.User(
        password=get_password_hash(user.password),
        username=user.username,
        email=user.email,
        age=user.age,
        location=user.location
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="This username already exists, please use another one"
                )
