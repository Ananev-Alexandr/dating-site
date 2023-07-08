from sqlalchemy import update
from sqlalchemy.orm import Session

from app.database.models.user_models import User
from app.routers.users.crud import get_user


def update_user(
        id,
        data_to_update,
        db: Session
        ) -> list:

    dict_to_update = {}

    if data_to_update.username:
        dict_to_update["username"] = data_to_update.username
    if data_to_update.email:
        dict_to_update["email"] = data_to_update.email
    if data_to_update.age:
        dict_to_update["age"] = data_to_update.age
    if data_to_update.location:
        dict_to_update["location"] = data_to_update.location

    db.execute(
        update(User)
        .where(User.id == id)
        .values(dict_to_update)
    )

    db.commit()
    return get_user(id, db)
