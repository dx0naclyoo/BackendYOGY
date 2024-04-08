from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class EnumCustomerType(str, Enum):
    INNER = "Внутренний"
    EXTERNAL = "Внешний"


class Spheres(str, Enum):
    IT = "It"
    volunteering = "Волонтёрство"
    history = "История"
    logistics = "Логистика"


class Types(str, Enum):
    busines = "Бизнес"
    social = "Социальный"


class Identity(str, Enum):
    GREEN = "Green"
    LEAN = "Lean"
    SMART = "Smart"


class BaseProjects(BaseModel):
    count_place: int
    deadline_date: datetime
    customer_type: EnumCustomerType
    orders_id: int
    lecturer_id: int


class Projects(BaseProjects):
    id: int
    registration_date: datetime


class AddProjects(BaseProjects):
    pass


class ProjectsAddForUSER(BaseModel):
    name: str
    description: str
    user_id: int = None
    orders_id: int
