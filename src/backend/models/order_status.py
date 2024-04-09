from enum import Enum

from pydantic import BaseModel


class EnumOrderStatis(str, Enum):
    Processing = "В обработке"
    Accepted = "Принят"
    Completed = "Выполнен"
    Rejected = "Отклонён"


class BaseOrderStatus(BaseModel):
    name: EnumOrderStatis


class AddOrderStatus(BaseOrderStatus):
    pass


class OrderStatus(BaseOrderStatus):
    id: int
