from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.config import JWTSettings
from app.core.db.database import get_db
from app.core.db.models import User

from .schemas import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
jwt_settings = JWTSettings()

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


DUMMY_HASH = get_password_hash("dummypassword")


def authenticate_user(
    db: Annotated[Session, Depends(get_db)], username: str, password: str
):
    user = db.query(User).filter_by(email=username).first()
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15.0)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=jwt_settings.jwt_secret_key,
        algorithm=jwt_settings.jwt_algorithm,
    )
    return encoded_jwt


async def login_for_token(
    db: Session,
    form_data: OAuth2PasswordRequestForm,
) -> Token:

    user_dict = authenticate_user(db, form_data.username, form_data.password)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token_expiration = timedelta(minutes=jwt_settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user_dict.email}, expires_delta=token_expiration
    )
    return Token(access_token=access_token, token_type="bearer")
