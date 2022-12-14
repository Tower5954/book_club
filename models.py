from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Book:
    _id: str
    title: str
    author: str
    year: int
    characters: list[str] = field(default_factory=list)
    series: list[str] = field(default_factory=list)
    last_read: datetime = None
    rating: int = 0
    tags: list[str] = field(default_factory=list)
    description: str = None
    image_link:  str = None


@dataclass
class Bookworm:
    _id: str
    email: str
    password: str
    books: list[str] = field(default_factory=list)


@dataclass
class Bookworm:
    _id: str
    email: str
    password: str
    books: list[str] = field(default_factory=list)