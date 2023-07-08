from sqlalchemy import delete as delete_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.database.models.user_models import User


def delete_user(
        id,
        db: Session
        ) -> list:
    if db.query(User).filter(User.id == id).one_or_none() is None:
        raise HTTPException(status_code=404)
    try:
        db.execute(delete_(User).where(User.id == id))
        db.commit()
        return {"message": "User successfully deleted"}
    except IntegrityError as ex:
            raise HTTPException(
            status_code=500,
            detail=f"an unexpected error occurred: {ex}"
        )