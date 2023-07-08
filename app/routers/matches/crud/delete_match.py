from sqlalchemy import delete as delete_
from sqlalchemy.orm import Session

from app.database.models.matches_models import Match


def delete_match(
        id,
        db: Session
        ) -> list:
    db.execute(delete_(Match).where(Match.id == id))
    db.commit()
    return {"message": "Match successfully deleted"}
