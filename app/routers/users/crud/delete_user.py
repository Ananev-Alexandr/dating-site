from sqlalchemy import delete as delete_
from sqlalchemy.orm import Session

from app.database.models.user_models import User


def delete_user(
        id,
        db: Session
        ) -> list:
    db.execute(delete_(User).where(User.id == id))
    db.commit()
    return {"message": "User successfully deleted"}
