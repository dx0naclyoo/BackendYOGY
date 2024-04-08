from pydantic import BaseModel
from src.backend.models import auth

class Orders(BaseModel):
    id: int
    name: str
    description: str
    user_id: int


    class Config:
        from_attributes = True


class OrderAddForBackend(BaseModel):
    name: str
    description: str
    user_id: int = None
    status_id: int = None


class OrderAddForUSER(BaseModel):
    name: str
    description: str


class OrderStatus(BaseModel):
    id: int


class Comment(BaseModel):
    id: int



class OrderUpdate(BaseModel):
    name: str
    description: str
