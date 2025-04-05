from dataclasses import dataclass
from decimal import Decimal

from litestar.dto import DataclassDTO, DTOConfig


@dataclass
class GenresDTO:
    id: int
    name: str
    slug: str


@dataclass
class WriteGenreDTO:
    name: str


@dataclass
class BookDTO:
    id: int
    title: str
    slug: str
    price: Decimal
    description: str | None
    genre_id: int
    user_id: int

class BookResponseDTO(DataclassDTO[BookDTO]):
    config = DTOConfig(rename_strategy="lower")

@dataclass
class WriteBookRequest:
    title: str
    price: Decimal
    description: str | None
    genre_id: int
    def __post_init__(self):
        if len(self.title) > 255:
            raise ValueError("Title too long")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not isinstance(self.genre_id, int):
            raise ValueError("Genre ID must be integer")
class WriteBookDTO(DataclassDTO[WriteBookRequest]):
    config = DTOConfig(include={"title", "price", "description", "genre_id"})


@dataclass
class PatchBookRequest:
    title: str | None
    price: Decimal | None
    description: str | None
    genre_id: int | None

class PatchBookDTO(DataclassDTO[PatchBookRequest]):
    config = DTOConfig(partial=True)
