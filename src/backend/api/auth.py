from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.models import auth as models

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.get("/", response_model=models.User)
async def user():
    return "user"


@router.get("/login")
async def login():
    return "Login"


@router.get("/register")
async def register():
    return "Register"
