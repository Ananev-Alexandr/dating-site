import os
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.helpers.password import verify_password
from app.database.models import user_models
from app.database.db_connection import get_db
from app.authorization.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def login(db: Session, username: str, password: str):
    db_user = db.query(user_models.User).\
        filter(user_models.User.username == username).one_or_none()
    db_user_with_pass = db_user.password
    hash_pass = verify_password(password, str(db_user_with_pass))
    if db_user and hash_pass:
        return db_user
    raise HTTPException(status_code=401, detail="Login or password is wrong")


def create_access_token(
    data: dict,
    expires_delta: Union[timedelta, None] = None
        ) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv("SECRET_KEY2"),
        algorithm=os.getenv("ALGORITHM")
            )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
        ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY2"),
            algorithms=[os.getenv("ALGORITHM")]
                )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(user_models.User).\
        filter(user_models.User.username == token_data.username).one_or_none()
    if user is None:
        raise credentials_exception
    return user