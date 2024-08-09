import asyncio

import aiohttp
import yarl

import aiohttp_toolkit as aiohtk


class Client:
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()

    async def fetch(self, url: yarl.URL) -> None:
        out, err = await aiohtk.RequestHandler.request(
            session=self._session,
            response_callback=aiohtk.callbacks.text,
            response_callback_kwargs={},
            method="GET",
            url=url,
        )
        if err:
            raise err

        res = aiohtk.models.Text(**out)
        if not res.ok:
            raise RuntimeError(f"response is not ok: {res.status=}")

        print(repr(res))
        print(res.text)

    async def close(self) -> None:
        await self._session.close()


async def main() -> None:
    url1 = yarl.URL("https://example.com")
    url2 = yarl.URL("https://httpbin.org/get")

    client = Client()
    await client.fetch(url=url1)
    await client.fetch(url=url2)
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
