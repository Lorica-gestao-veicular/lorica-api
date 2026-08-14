from fastapi import APIRouter

from .schemas import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def get_users():
    users = []

    return users
