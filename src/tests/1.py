from enum import Enum


# string = "string".encode()
# print(type(string))


class UserRole(str, Enum):
    ADMIN: str = "Админ"
    STUDENT: str = "Студент"
    LECTURER: str = "Преподаватель"
    CUSTOMER: str = "Заказчик"
    UNDEFINED: str = "Нечто"


asd = [UserRole.ADMIN.value, UserRole.STUDENT.value]


