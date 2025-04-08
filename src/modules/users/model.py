from typing import TYPE_CHECKING

from litestar.dto import dto_field
from sqlalchemy import String, DECIMAL, DefaultClause, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.modules.users.role import UserRole

if TYPE_CHECKING:
    from src.modules.books.model import BookDb
from src.infrastructure.database import BaseDB


class UserDb(BaseDB):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(length=255), unique=True, nullable=False
    )
    deposit: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=10, scale=2),
        default=0,
        server_default=DefaultClause("0.00"),
    )
    password: Mapped[str] = mapped_column(String(length=255), nullable=False, info=dto_field("private"))
    is_activate: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.user)

    books: Mapped[list["BookDb"]] = relationship(back_populates="user", info=dto_field("read-only"),lazy="selectin")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"

    def __str__(self) -> str:
        return self.email
