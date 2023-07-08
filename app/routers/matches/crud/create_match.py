from sqlalchemy.orm import Session

from app.database.models import matches_models, user_models
from app.routers.matches.schemas import MatchCreate


def create_match(db: Session, match: MatchCreate):
    db_match = matches_models.Match(
        user1_id=match.user1_id,
        user2_id=match.user2_id,
    )
    if db.query(user_models.User)\
        .filter(user_models.User.id == match.user1_id).one_or_none() and\
        db.query(user_models.User)\
            .filter(user_models.User.id == match.user2_id).one_or_none():
        db.add(db_match)
        db.commit()
        db.refresh(db_match)
        return db_match
