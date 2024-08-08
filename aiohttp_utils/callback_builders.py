from typing import Any, Optional, Union

import aiohttp as _aiohttp

from .types import CbBuilderOut


__all__ = (
    "status",
    "headers",
    "cookies",
    "read",
    "text",
    "json",
    "close",
)


async def status(
    data: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    """
    Status callback builder.

    Adds `status (str)` and `ok (bool)` fields to handled data
    """

    data |= dict(
        status=cr.status,
        ok=cr.ok,
    )

    return data, None


async def headers(
    data: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    """
    Headers callback builder.

    Adds `headers (multidict.CIMultiDictProxy[str])` field to handled data
    """

    data |= dict(
        headers=cr.headers,
    )

    return data, None


async def cookies(
    data: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    """
    Cookies callback builder.

    Adds `cookies (http.cookies.SimpleCookie)` field to handled data
    """

    data |= dict(
        cookies=cr.cookies,
    )

    return data, None


async def read(
    data: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    """
    Read callback builder.

    Adds `read (bytes)` field to handled data
    """

    read: bytes
    try:
        read = await cr.read()
    except Exception as err:
        return data, err

    data |= dict(
        read=read,
    )

    return data, None


async def text(
    data: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    """
    Text callback builder.

    Adds `text (str)` field to handled data.

    Takes kwargs by `"text"` key from parent kwargs and unpacks as
    `aiohttp.ClientResponse.text(**kwargs)`
    """

    kwargs = kwargs.get("text", {})

    text: str
    try:
        text = await cr.text(**kwargs)
    except Exception as err:
        return data, err

    data |= dict(
        text=text,
    )

    return data, None


async def json(
    data: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    """
    Json callback builder.

    Adds `json (Any)` field to handled data.

    Takes kwargs by `"json"` key from parent kwargs and unpacks as
    `aiohttp.ClientResponse.json(**kwargs)`
    """

    kwargs = kwargs.get("json", {})

    json: Union[dict[str, Any], list[Any], Any]
    try:
        json = await cr.json(**kwargs)
    except Exception as err:
        return data, err

    data |= dict(
        json=json,
    )

    return data, None


async def close(
    data: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    """
    Close callback builder.

    A special callback builder that is used to close ahead
    `aiohttp.ClientResponse` to release resources
    """

    cr.release()
    await cr.wait_for_close()

    return data, None
