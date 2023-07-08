import os
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.db_connection import get_db
from app.enums import SortEnum
from app.routers.users import crud, schemas
from app.authorization.schemas import Token
from app.authorization import services

router = APIRouter(tags=["Users"])


@router.post("/token", response_model=Token, include_in_schema=False)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
        ):
    user = services.login(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
    access_token = services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/")
async def get_all_users(
    sort_username: SortEnum,
    sort_email: SortEnum,
    age_filters: int | None = None,
    location_filters: str | None = None,
    db: Session = Depends(get_db),
    authorization=Depends(services.get_current_user)
        ):
    users_list = crud.get_all_users(
        age_filters=age_filters,
        location_filters=location_filters,
        sort_username=sort_username,
        sort_email=sort_email,
        db=db
        )
    return JSONResponse(content=jsonable_encoder({"users": users_list}))


@router.post("/users/", response_model=schemas.UserOut)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=schemas.UserOut)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    authorization=Depends(services.get_current_user),
        ):
    return crud.get_user(id=user_id, db=db)


@router.put("/users/{user_id}", response_model=schemas.UserOut)
async def update_user(
    user_id: int,
    data_to_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    authorization=Depends(services.get_current_user),
        ):
    return crud.update_user(
        id=user_id,
        db=db,
        data_to_update=data_to_update,
        )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    authorization=Depends(services.get_current_user),
        ):
    return crud.delete_user(id=user_id, db=db)
