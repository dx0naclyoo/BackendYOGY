from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.get("/")
async def user():
    return "user"


@router.get("/login")
async def login():
    return "Login"


@router.get("/register")
async def register():
    return "Register"
