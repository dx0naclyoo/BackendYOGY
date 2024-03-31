from pydantic import BaseModel


class Role(BaseModel):
    id: int
    name: str


class UserBase(BaseModel):
    username: str


class UserRegister(UserBase):
    password: str


class User(UserBase):
    id: int



class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
