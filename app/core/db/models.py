from sqlalchemy.orm import DeclarativeBase

from app.features.users.models import UserModel


class Base(DeclarativeBase):
    pass


class User(Base, UserModel):
    pass
