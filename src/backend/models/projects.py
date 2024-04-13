from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel
from src.backend.models import auth as auth_models


class EnumCustomerType(str, Enum):
    INNER = "Внутренний"
    EXTERNAL = "Внешний"


class EnumSpheres(str, Enum):
    IT = "IT"
    Volunteering = "Волонтёрство"
    Journalism = "Журналистика"
    History = "История"
    Logistics = "Логистика"
    Marketing = "Маркетинг"
    Education = "Образование"
    Social_media = "SocialMedia"
    Economy = "Экономика"
    Jurisprudence = "Юриспруденция"


class EnumTypes(str, Enum):
    Business = "Бизнес"
    Social = "Социальный"
    Creative = "Творческий"
    Research = "Исследовательский"


class EnumIdentity(str, Enum):
    GREEN = "Green"
    LEAN = "Lean"
    SMART = "Smart"


class BaseProjects(BaseModel):
    count_place: int
    deadline_date: datetime
    order_id: int
    customer_type: EnumCustomerType
    identity: List[EnumIdentity]
    types: List[EnumTypes]
    spheres: List[EnumSpheres]


class Projects(BaseProjects):
    name: str
    description: str
    id: int
    registration_date: datetime
    lecturer: auth_models.User


class AddProjects(BaseProjects):
    lecturer_id: int



