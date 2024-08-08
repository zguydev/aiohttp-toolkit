from typing import Any
import dataclasses
import http.cookies

import multidict


__all__ = (
    "Status", "Properties", "Read", "Text", "JsonObj", "JsonList", "JsonAny",
)


@dataclasses.dataclass
class Status:
    """
    `Status` - used to be applied from `status` callback.
    """
    
    status: int
    ok: bool


@dataclasses.dataclass
class Properties(Status):
    """
    `Properties` - used to be applied from `properties` callback.
    Inherits `Status`.
    """
    
    headers: multidict.CIMultiDictProxy[str]
    cookies: http.cookies.BaseCookie


@dataclasses.dataclass
class Read(Properties):
    """
    `Read` - used to be applied from `read` callback.
    Inherits `Properties`.
    """
    
    read: bytes


@dataclasses.dataclass
class Text(Properties):
    """
    `Text` - used to be applied from `text` callback.
    Inherits `Properties`.
    """
    
    text: str


@dataclasses.dataclass
class JsonObj(Properties):
    """
    `JsonObj` - used to be applied from `json` callback, when JSON
    `object` is expected to be returned.
    Inherits `Properties`.
    """
    
    json: dict[str, Any]


@dataclasses.dataclass
class JsonList(Properties):
    """
    `JsonList` - used to be applied from `json` callback, when JSON
    `list` is expected to be returned.
    Inherits `Properties`.
    """
    
    json: list[Any]


@dataclasses.dataclass
class JsonAny(Properties):
    """
    `JsonAny` - used to be applied from `json` callback, when `any` JSON
    structure is expected to be returned, for example `number` or `null`.
    Inherits `Properties`.
    """
    
    json: Any
