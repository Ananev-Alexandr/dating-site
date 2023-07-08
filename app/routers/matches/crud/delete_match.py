from sqlalchemy import delete as delete_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.database.models.matches_models import Match


def delete_match(
        id,
        db: Session
        ) -> list:
    try:
        db.execute(delete_(Match).where(Match.id == id))
        db.commit()
        return {"message": "Match successfully deleted"}
    except IntegrityError as ex:
            raise HTTPException(
            status_code=500,
            detail=f"an unexpected error occurred: {ex}"
        )