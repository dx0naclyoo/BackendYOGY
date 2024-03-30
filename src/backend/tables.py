from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, LargeBinary, ForeignKey


class Base(DeclarativeBase): ...


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)

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
