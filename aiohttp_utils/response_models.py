from typing import Any
import dataclasses


@dataclasses.dataclass
class Status:
    status: int
    ok: bool


@dataclasses.dataclass
class Read(Status):
    read: bytes


@dataclasses.dataclass
class Text(Status):
    text: str


@dataclasses.dataclass
class Json(Status):
    json: dict[str, Any]


@dataclasses.dataclass
class JsonList(Status):
    json: list[Any]
