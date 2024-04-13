from enum import Enum
from typing import List

from pydantic import BaseModel
from datetime import datetime
from datetime import timedelta
# string = "string".encode()
# print(type(string))


# class UserRole(str, Enum):
#     ADMIN: str = "Админ"
#     STUDENT: str = "Студент"
#     LECTURER: str = "Преподаватель"
#     CUSTOMER: str = "Заказчик"
#     UNDEFINED: str = "Нечто"
#
#
# asd = [UserRole.ADMIN, UserRole.STUDENT]
#
# dsa = " ".join(asd)
#
# print(dsa.split(" "))

data = datetime.now() - timedelta(days=1)
print(data)

new_data = data.strftime("%d.%m.%Y, %H:%M:%S")
print(new_data)


class Proj(BaseModel):
    time: datetime | str

asd = Proj(time=new_data)
print(asd)

