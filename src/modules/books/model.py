from sqlalchemy import String, DefaultClause, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database import BaseDB
from src.modules.users.model import UserDb


class GenresDb(BaseDB):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(length=255), unique=True, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<Genre(id={self.id}, name='{self.name}')>"

    def __str__(self) -> str:
        return self.name


class BookDb(BaseDB):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=255), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(length=255), unique=True, nullable=False, index=True)
    price: Mapped[DECIMAL] = mapped_column(
        DECIMAL(precision=10, scale=2),
        default=0,
        server_default=DefaultClause("0.00")
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    genre: Mapped["GenresDb"] = relationship(lazy="selectin")
    user: Mapped["UserDb"] = relationship(back_populates="books",lazy="selectin")

    def __repr__(self) -> str:
        return f"<Book(id={self.id}, title='{self.title}')>"

    def __str__(self) -> str:
        return self.title
