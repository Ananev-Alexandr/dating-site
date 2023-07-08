from sqlalchemy import select
from sqlalchemy.orm import Session

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
    return result["User"]
