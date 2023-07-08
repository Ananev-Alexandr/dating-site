from sqlalchemy.orm import Session

from app.database.models.matches_models import Match


def get_all_matches(
        sort,
        db: Session
        ) -> list:
    query = db.query(Match)
    query = sort_matches(
        sort=sort,
        query=query,
    )
    return query.all()


def sort_matches(
        query,
        sort,
        ):
    if sort.name == "ASK":
        query = query.order_by(Match.match_date.asc())
    if sort.name == "DESK":
        query = query.order_by(Match.match_date.desc())
    return query
