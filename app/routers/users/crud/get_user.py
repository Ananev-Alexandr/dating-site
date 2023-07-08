from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.database.models.user_models import User


def get_user(
        id,
        db: Session
        ) -> list:
    query = (
        select(User)
        .select_from(User)
        .where(User.id == id)
    )
    result = db.execute(query).mappings().one_or_none()
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"User not found"
        )
    return result["User"]
