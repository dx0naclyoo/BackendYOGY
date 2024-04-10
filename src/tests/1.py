from enum import Enum
from typing import List


# string = "string".encode()
# print(type(string))


class UserRole(str, Enum):
    ADMIN: str = "Админ"
    STUDENT: str = "Студент"
    LECTURER: str = "Преподаватель"
    CUSTOMER: str = "Заказчик"
    UNDEFINED: str = "Нечто"


asd = [UserRole.ADMIN, UserRole.STUDENT]

dsa = " ".join(asd)

print(dsa.split(" "))
