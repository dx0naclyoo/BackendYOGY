from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class EnumCustomerType(str, Enum):
    INNER = "Внутренний"
    EXTERNAL = "Внешний"


class EnumSpheres(str, Enum):
    IT = "It"
    volunteering = "Волонтёрство"
    history = "История"
    logistics = "Логистика"


class EnumTypes(str, Enum):
    busines = "Бизнес"
    social = "Социальный"


class EnumIdentity(str, Enum):
    GREEN = "Green"
    LEAN = "Lean"
    SMART = "Smart"


class BaseProjects(BaseModel):
    count_place: int
    deadline_date: datetime
    order_id: int
    lecturer_id: int
    customer_type: EnumCustomerType
    identity: List[EnumIdentity]
    types: List[EnumTypes]
    spheres: List[EnumSpheres]


class Projects(BaseProjects):
    id: int
    registration_date: datetime



class AddProjects(BaseProjects):
    pass



