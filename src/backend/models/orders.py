from pydantic import BaseModel


class Orders(BaseModel):
    id: int
    name: str
    description: str
    user: str




class OrderStatus(BaseModel):
    id: int


class Comment(BaseModel):
    id: int
