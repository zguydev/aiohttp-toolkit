from typing import Any, Optional, Union

import aiohttp


@staticmethod
async def status(
    client_response: aiohttp.ClientResponse,
    **kwargs,
) -> tuple[dict[str, Any], None]:
    r = client_response

    out: dict[str, Any] = {}

    out |= dict(
        status=r.status,
        ok=r.ok,
    )

    return out, None

@staticmethod
async def read(
    client_response: aiohttp.ClientResponse,
    **kwargs,
) -> tuple[dict[str, Any], Optional[Exception]]:
    r = client_response

    out: dict[str, Any] = {}

    out_partial, _ = await status(
        client_response=client_response,
        **kwargs,
    )
    out |= out_partial

    read: bytes
    try:
        read = await r.read()
    except Exception as err:
        return out, err

    out |= dict(
        read=read,
    )

    return out, None

@staticmethod
async def text(
    client_response: aiohttp.ClientResponse,
    **kwargs,
) -> tuple[dict[str, Any], Optional[Exception]]:
    r = client_response

    out: dict[str, Any] = {}

    out_partial, _ = await status(
        client_response=client_response,
        **kwargs,
    )
    out |= out_partial

    text: str
    try:
        text = await r.text()
    except Exception as err:
        return out, err

    out |= dict(
        text=text,
    )

    return out, None
