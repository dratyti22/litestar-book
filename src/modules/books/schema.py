from dataclasses import dataclass
from decimal import Decimal


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
    description: str
    genre_id: int
    user_id: int
