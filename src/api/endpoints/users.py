from fastapi import APIRouter, status

from src.schemas.users import CreateUser


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="create user",
)
async def register(user: CreateUser):
    return {
        "message": "User created",
        "user": user,
    }

