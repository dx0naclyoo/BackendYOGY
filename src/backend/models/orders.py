from pydantic import BaseModel
from src.backend.models import order_status


class Orders(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    status: order_status.OrderStatus

    class Config:
        from_attributes = True


class OrderAddForBackend(BaseModel):
    name: str
    description: str
    user_id: int
    status_id: int


class OrderAddForUSER(BaseModel):
    name: str
    description: str

# class Comment(BaseModel):
#     id: int


class OrderUpdate(BaseModel):
    name: str
    description: str
