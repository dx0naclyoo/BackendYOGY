from pydantic import BaseModel
from src.backend.models import auth as auth_models


class Letter(BaseModel):
    id: int
    text: str
    user: auth_models.User
    project_id: int


class AddLetter(BaseModel):
    text: str


class DeleteLetter(Letter):
    pass