from pydantic import BaseModel

from sqlalchemy import DateTime, Enum


class EnumCustomerType(str, Enum):
    INNER = "Внутренний"
    EXTERNAL = "Внешний"


class Projects(BaseModel):
    id: int
    count_place: int
    registration_date: DateTime
    deadline_date: DateTime
    customer_type: EnumCustomerType
    orders_id: int
    user_id: int
    types_id: int | None = None
    direction_identity_id: int | None = None
    spheres_id: int | None = None
    tags_id: int | None = None


class ProjectsAddForBackend(BaseModel):
    name: str
    count_place: int
    registration_date: DateTime
    deadline_date: DateTime
    customer_type: EnumCustomerType
    orders_id: int
    user_id: int



class ProjectsAddForUSER(BaseModel):
    name: str
    description: str
    user_id: int = None
    orders_id: int


