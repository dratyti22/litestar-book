from dataclasses import dataclass



@dataclass
class GenresDTO:
    id: int
    name: str
    slug: str


@dataclass
class WriteGenreDTO:
    name: str


