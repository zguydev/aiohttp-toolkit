from typing import Any, Optional, Union

import aiohttp as _aiohttp

from ._types import CbBuilderOut


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
    out: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    out |= dict(
        status=cr.status,
        ok=cr.ok,
    )

    return out, None


async def headers(
    out: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    out |= dict(
        headers=cr.headers,
    )

    return out, None


async def cookies(
    out: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    out |= dict(
        cookies=cr.cookies,
    )

    return out, None


async def read(
    out: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    read: bytes
    try:
        read = await cr.read()
    except Exception as err:
        return out, err

    out |= dict(
        read=read,
    )

    return out, None


async def text(
    out: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    kwargs = kwargs.get("text", {})

    text: str
    try:
        text = await cr.text(**kwargs)
    except Exception as err:
        return out, err

    out |= dict(
        text=text,
    )

    return out, None


async def json(
    out: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    kwargs = kwargs.get("json", {})

    json: Union[dict[str, Any], list[Any], Any]
    try:
        json = await cr.json(**kwargs)
    except Exception as err:
        return out, err

    out |= dict(
        json=json,
    )

    return out, None


async def close(
    out: dict[str, Any],
    cr: _aiohttp.ClientResponse,
    **kwargs,
) -> CbBuilderOut:
    cr.release()
    await cr.wait_for_close()
    
    return out, None
