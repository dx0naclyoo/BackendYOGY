from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, ForeignKey
from sqlalchemy import Integer, Text, LargeBinary


class Base(DeclarativeBase): ...


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("userrole.id"))
    role: Mapped["UserRole"] = relationship(back_populates="user")


class UserRole(Base):
    __tablename__ = "userrole"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="role")
