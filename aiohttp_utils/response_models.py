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
