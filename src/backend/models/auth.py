from enum import Enum
from typing import List

from pydantic import BaseModel

from src.backend.models import role as role_models


class UserBase(BaseModel):
    username: str


class UserRegister(UserBase):
    password: str


class User(UserBase):
    id: int
    roles: List[role_models.EnumBackendRole]


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
