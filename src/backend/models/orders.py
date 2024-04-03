from pydantic import BaseModel


class Orders(BaseModel):
    id: int
    name: str
    description: str
    user: str

class OrderAdd(BaseModel):
    name: str
    description: str
    user_id: int = None
    status_id: int = None


class OrderStatus(BaseModel):
    id: int


class Comment(BaseModel):
    id: int
