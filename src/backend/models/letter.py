from pydantic import BaseModel
from src.backend.models import auth as auth_models


class Letter(BaseModel):
    text: str
    user: auth_models.User


class AddLetter(BaseModel):
    text: str

