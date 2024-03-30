from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.models import auth as models

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.get("/{user_id}")
async def user(user_id: int):
    return user_id
    # return models.User(id=user_id, username="Ivan", role={"id": 1, "name": "ADMIN"})



@router.get("/login")
async def login():
    return "Login"


@router.get("/register")
async def register():
    return "Register"
