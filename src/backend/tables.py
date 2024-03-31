from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, LargeBinary, ForeignKey


class Base(DeclarativeBase): ...


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)

    orders: Mapped["Orders"] = relationship(back_populates="user", uselist=True)

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

    comment_id: Mapped[int] = mapped_column(ForeignKey("comment.id"))
    comment: Mapped["Comment"] = relationship(back_populates="order", uselist=False)

    status_id: Mapped[int] = mapped_column(ForeignKey("order_status.id"), nullable=False)
    status: Mapped["OrderStatus"] = relationship(back_populates="order", uselist=False)


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


