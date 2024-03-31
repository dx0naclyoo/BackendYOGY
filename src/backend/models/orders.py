from pydantic import BaseModel


class Orders(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    comment_id: int | None
    status_id: int

class OrderAdd(BaseModel):
    name: str
    description: str
    user_id: int = None
    status_id: int = None

class OrderStatus(BaseModel):
    id: int
    name: str



class Comment(BaseModel):
    id: int
    text: str
