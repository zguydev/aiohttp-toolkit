from typing import Any
import dataclasses
import http.cookies

import multidict


@dataclasses.dataclass
class Status:
    status: int
    ok: bool


@dataclasses.dataclass
class Info(Status):
    headers: multidict.CIMultiDictProxy[str]
    cookies: http.cookies.BaseCookie


@dataclasses.dataclass
class Read(Info):
    read: bytes


@dataclasses.dataclass
class Text(Info):
    text: str


@dataclasses.dataclass
class JsonObj(Info):
    json: dict[str, Any]


@dataclasses.dataclass
class JsonList(Info):
    json: list[Any]


@dataclasses.dataclass
class JsonAny(Info):
    json: Any
