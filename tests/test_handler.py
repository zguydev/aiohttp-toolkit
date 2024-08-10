from typing import Any
from unittest.mock import MagicMock

import aiohttp
import aiohttp.test_utils
import pytest
import yarl

import aiohttp_toolkit as aiohtk


@pytest.mark.asyncio
async def test_prepare_request(
    shared: dict[str, Any],
) -> None:
    mock_session = MagicMock(aiohttp.ClientSession)

    mock_request_context = MagicMock()
    mock_session.request.return_value = mock_request_context

    method = "GET"
    url: yarl.URL = shared["test_server_url"]
    params = {"key": "value"}
    headers = headers = {
        "Authorization": "Bearer token",
        "User-Agent": "aiohttp",
    }

    mock_request_context = aiohtk.RequestHandler._prepare_request(
        session=mock_session,
        method=method,
        url=url,
        params=params,
        headers=headers,
    )

    mock_session.request.assert_called_once_with(
        method=method,
        url=url,
        params=params,
        data=None,
        json=None,
        cookies=None,
        headers=headers,
        skip_auto_headers=None,
        auth=None,
        allow_redirects=True,
        max_redirects=10,
        compress=None,
        chunked=None,
        expect100=False,
        raise_for_status=None,
        read_until_eof=True,
        proxy=None,
        proxy_auth=None,
        timeout=aiohttp.helpers.sentinel,
        ssl=True,
        server_hostname=None,
        proxy_headers=None,
        trace_request_ctx=None,
        read_bufsize=None,
        auto_decompress=None,
        max_line_size=None,
        max_field_size=None,
        verify_ssl=None,
        fingerprint=None,
        ssl_context=None,
    )

    assert mock_request_context == mock_request_context

@pytest.mark.asyncio
async def test_process_request(
    shared: dict[str, Any],
    aiohttp_test_server: aiohttp.test_utils.TestServer,
    aiohttp_session: aiohttp.ClientSession,
) -> None:
    method = "GET"
    url: yarl.URL = shared["test_server_url"]
    params = {"key": "value"}
    headers = {
        "Authorization": "Bearer token",
        "User-Agent": "aiohttp",
    }

    request_context = aiohtk.RequestHandler._prepare_request(
        session=aiohttp_session,
        method=method,
        url=url,
        params=params,
        headers=headers,
    )

    callback = aiohtk.callbacks.json
    callback_kwargs = {}

    out, err = await aiohtk.RequestHandler._process_request(
        request_context=request_context,
        response_callback=callback,
        **callback_kwargs,
    )
    if err:
        raise err

    expected_response_json = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Authorization": "Bearer token",
        "Host": f"{url.host}:{url.port}",
        "User-Agent": "aiohttp",
    }

    assert out.get("status") == 200
    assert out.get("headers", {}).get("Content-Type") == "application/json"
    assert out.get("json") == expected_response_json

@pytest.mark.asyncio
async def test_client(
    shared: dict[str, Any],
    aiohttp_test_server: aiohttp.test_utils.TestServer,
    aiohttp_session: aiohttp.ClientSession,
) -> None:
    callback = aiohtk.callbacks.read
    callback_kwargs = {}
    model = aiohtk.models.Read
    method = "POST"
    url: yarl.URL = shared["test_server_url"]
    data = b"Hello, World!"

    out, err = await aiohtk.RequestHandler.request(
        session=aiohttp_session,
        response_callback=callback,
        response_callback_kwargs=callback_kwargs,
        method=method,
        url=url,
        data=data,
    )
    if err:
        raise err

    res = model(**out)
    if not res.ok:
        raise RuntimeError(f"response is not ok: {res.status=}")

    assert res.read == data
