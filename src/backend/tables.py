from datetime import datetime

from sqlalchemy import Text, ForeignKey, DateTime, TIMESTAMP, func, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.backend.models import projects as projects_models
from src.backend.models import role as role_models


# from enum import Enum
# from typing import List


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)

    roles: Mapped[list["Role"]] = relationship(back_populates="users",
                                               uselist=True,
                                               secondary="user_role",
                                               lazy="selectin")

    student_projects: Mapped[list["Projects"]] = relationship(back_populates="students",
                                                              uselist=True,
                                                              secondary="project_user",
                                                              lazy="selectin")

    # project: Mapped["Projects"] = relationship(back_populates="lecturers", uselist=True, lazy="joined")

    motivation_letters: Mapped["MotivationLetters"] = relationship(back_populates="user", uselist=True)

    orders: Mapped["Orders"] = relationship(back_populates="user", uselist=True)

    projects: Mapped["Projects"] = relationship(back_populates="lecturers", uselist=True, lazy="joined")

    # lecturer_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    # lecturers: Mapped["User"] = relationship(back_populates="projects",
    #                                          uselist=False)

class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped["role_models.EnumBackendRole"] = mapped_column(String, nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="roles",
                                               uselist=True,
                                               secondary="user_role",
                                               lazy="selectin")


class SecondaryUserRole(Base):
    __tablename__ = "user_role"
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    count_place: Mapped[int] = mapped_column(Integer, nullable=False, )
    registration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deadline_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    customer_type: Mapped[str] = mapped_column(Text,
                                               nullable=False,
                                               default=projects_models.EnumCustomerType.INNER)

    # Связь студентов с проектами
    students: Mapped[list["User"]] = relationship(back_populates="student_projects",
                                                  uselist=True,
                                                  secondary="project_user",
                                                  lazy="joined")

    # ForeignKey на заказ
    orders_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    orders: Mapped["Orders"] = relationship(back_populates="projects", uselist=False)

    # Руководитель
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    lecturers: Mapped["User"] = relationship(back_populates="projects",
                                             uselist=False)

    # Вид проекта
    types_id: Mapped[int] = mapped_column(ForeignKey("types.id"), nullable=False)
    types: Mapped["Types"] = relationship(back_populates="projects", uselist=False)

    # Направление идентичности ЮГУ
    direction_identity_id: Mapped[int] = mapped_column(ForeignKey("direction_identity.id"), nullable=False)
    direction_identity: Mapped["DirectionIdentity"] = relationship(back_populates="projects", uselist=False)

    # Сферы проекта
    spheres_id: Mapped[int] = mapped_column(ForeignKey("spheres.id"), nullable=False)
    spheres: Mapped["Spheres"] = relationship(back_populates="projects", uselist=False)

    # Тэги проекта
    # tags_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=False)
    # tags: Mapped["Tags"] = relationship(back_populates="projects", uselist=False)

    # Мотивационные письма
    motivation_letters: Mapped["MotivationLetters"] = relationship(back_populates="projects", uselist=False)


class SecondaryProjectUser(Base):
    __tablename__ = "project_user"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    projects_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)

    registration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MotivationLetters(Base):
    __tablename__ = "motivation_letters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="motivation_letters", uselist=False)

    projects_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    projects: Mapped["Projects"] = relationship(back_populates="motivation_letters", uselist=True)


class AbstractProjectCharacteristics(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)


class DirectionIdentity(AbstractProjectCharacteristics):
    __tablename__ = "direction_identity"

    projects: Mapped["Projects"] = relationship(back_populates="direction_identity", uselist=True)


class Spheres(AbstractProjectCharacteristics):
    __tablename__ = "spheres"

    projects: Mapped["Projects"] = relationship(back_populates="spheres", uselist=True)


class Types(AbstractProjectCharacteristics):
    __tablename__ = "types"

    projects: Mapped["Projects"] = relationship(back_populates="types", uselist=True)


# class Tags(AbstractProjectCharacteristics):
#     __tablename__ = "tags"
#
#     projects: Mapped["Projects"] = relationship(back_populates="tags", uselist=True)


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="orders", uselist=False)

    comment_id: Mapped[int] = mapped_column(ForeignKey("comment.id"), nullable=True)
    comment: Mapped["Comment"] = relationship(back_populates="order", uselist=False)

    status_id: Mapped[int] = mapped_column(ForeignKey("order_status.id"), nullable=False)
    status: Mapped["OrderStatus"] = relationship(back_populates="order", uselist=False)

    projects: Mapped["Projects"] = relationship(back_populates="orders", uselist=False)


class OrderStatus(Base):
    __tablename__ = "order_status"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    order: Mapped["Orders"] = relationship(back_populates="status", uselist=True)


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    order: Mapped["Orders"] = relationship(back_populates="comment", uselist=False)
