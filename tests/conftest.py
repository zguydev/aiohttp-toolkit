from typing import Any, AsyncGenerator
import json

import aiohttp
import aiohttp.test_utils
import multidict
import pytest
import pytest_asyncio
import yarl
from aiohttp import web

from . import config


@pytest.fixture(scope="session")
def shared() -> dict[str, Any]:
    """fixture to share variables between tests"""

    shared: dict[str, Any] = {}

    shared.update(dict(
        test_server_url = yarl.URL.build(
            scheme="http",
            host="127.0.0.1",
            port=config.TEST_SERVER_PORT,
        ),
    ))

    return shared

@pytest_asyncio.fixture(scope="function")
async def aiohttp_test_server() -> AsyncGenerator[aiohttp.test_utils.TestServer, Any]:
    async def handle_get(request: web.Request) -> web.Response:
        raw_headers = multidict.CIMultiDict(request.headers)
        headers = {
            k: ",".join(raw_headers.getall(k))
            for k in raw_headers.keys()
        }

        return web.Response(
            body=json.dumps(headers, separators=(",", ":")),
            content_type="application/json",
        )

    async def handle_post(request: web.Request) -> web.Response:
        return web.Response(body=await request.read())

    app = web.Application()
    app.router.add_get("/", handle_get)
    app.router.add_post("/", handle_post)
    server = aiohttp.test_utils.TestServer(
        app=app,
        scheme="http",
        host="127.0.0.1",
        port=config.TEST_SERVER_PORT,
    )
    await server.start_server()

    yield server

    await server.close()

# BUG: this fixture with scope="session" fails, as session spawns not as a task. It is prefered so the aiohttp.ClientSession was created once, not for every function
# @pytest_asyncio.fixture(scope="session")
@pytest_asyncio.fixture(scope="function")
async def aiohttp_session() -> AsyncGenerator[aiohttp.ClientSession, Any]:
    session = aiohttp.ClientSession()

    yield session

    await session.close()
