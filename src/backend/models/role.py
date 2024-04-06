from enum import Enum

from pydantic import BaseModel


class EnumBackendRole(str, Enum):
    ADMIN = "Admin"
    STUDENT = "Student"
    LECTURER = "Lecturer"
    CUSTOMER = "Customer"
    UNDEFINED = "Undefined"


class EnumUserViewRole(str, Enum):
    STUDENT = "Student"
    LECTURER = "Lecturer"
    CUSTOMER = "Customer"


class Role(BaseModel):
    id: int
    name: EnumBackendRole


class ADDRole(BaseModel):
    name: EnumBackendRole


