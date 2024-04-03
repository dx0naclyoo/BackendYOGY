from datetime import datetime
from enum import Enum

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, LargeBinary, ForeignKey, DateTime, TIMESTAMP, func


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)

    connection: Mapped["Connection"] = relationship(back_populates="user", uselist=True)

    motivation_letters: Mapped["MotivationLetters"] = relationship(back_populates="user", uselist=True)

    orders: Mapped["Orders"] = relationship(back_populates="user", uselist=True)

    projects: Mapped["Projects"] = relationship(back_populates="user", uselist=True)

    roles: Mapped[list["Role"]] = relationship(back_populates="users", uselist=True, secondary="user_role")




class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="roles", uselist=True, secondary="user_role")


class SecondaryUserRole(Base):
    __tablename__ = "user_role"
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)


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


class CustomerType(str, Enum):
    INNER = "Внутренний"
    EXTERNAL = "Внешний"


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    countPlace: Mapped[int]
    registration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deadline_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    customer_type: Mapped["CustomerType"] = mapped_column(Text, nullable=False, default=CustomerType.INNER)

    # Связь студентов с проектами
    connection: Mapped["Connection"] = relationship(back_populates="projects", uselist=False)

    # ForeignKey на заказ
    orders_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    orders: Mapped["Orders"] = relationship(back_populates="projects", uselist=False)

    # Руководитель
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="projects", uselist=False)

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
    tags_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=False)
    tags: Mapped["Tags"] = relationship(back_populates="projects", uselist=False)

    # Мотивационные письма
    motivation_letters: Mapped["MotivationLetters"] = relationship(back_populates="projects", uselist=False)


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


class Tags(AbstractProjectCharacteristics):
    __tablename__ = "tags"

    projects: Mapped["Projects"] = relationship(back_populates="tags", uselist=True)


class Connection(Base):
    __tablename__ = "connection"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="connection", uselist=False)

    projects_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    projects: Mapped["Projects"] = relationship(back_populates="connection", uselist=True)


class MotivationLetters(Base):
    __tablename__ = "motivation_letters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="motivation_letters", uselist=False)

    projects_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    projects: Mapped["Projects"] = relationship(back_populates="motivation_letters", uselist=True)
