from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.user_models import User


def get_all_users(
        sort_username,
        sort_email,
        age_filters,
        location_filters,
        db: Session
        ) -> list:
    query = (
        select(
            User.id,
            User.username,
            User.email,
            User.age,
            User.location
            )
        .select_from(User)
    )
    query = sort_and_filter_users(
        query=query,
        sort_email=sort_email,
        sort_username=sort_username,
        age_filters=age_filters,
        location_filters=location_filters,
    )
    result = db.execute(query).mappings().all()
    return result


def sort_and_filter_users(
        query,
        sort_username,
        sort_email,
        age_filters,
        location_filters,
        ):
    if sort_username.name == "ASK":
        query = query.order_by(User.username.asc())
    if sort_username.name == "DESK":
        query = query.order_by(User.username.desc())
    if sort_email.name == "ASK":
        query = query.order_by(User.email.asc())
    if sort_email.name == "DESK":
        query = query.order_by(User.email.desc())
    if age_filters:
        query = query.where(User.age == age_filters)
    if location_filters:
        query = query.where(User.location.ilike(f"%{location_filters}%"))

    return query
