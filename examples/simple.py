import asyncio

import aiohttp
import yarl

import aiohttp_toolkit as aiohtk


async def main() -> None:
    url = yarl.URL("https://example.com")

    async with aiohttp.ClientSession() as session:
        out, err = await aiohtk.RequestHandler.request(
            session=session,
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


if __name__ == "__main__":
    asyncio.run(main())
