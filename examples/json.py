import asyncio

import aiohttp
import yarl

import aiohttp_utils as aiohu


async def main() -> None:
    url = yarl.URL("https://httpbin.dev/json")

    async with aiohttp.ClientSession() as session:
        out, err = await aiohu.RequestHandler.request(
            session=session,
            response_callback=aiohu.callbacks.json,
            response_callback_kwargs={},
            method="GET",
            url=url,
        )
        if err:
            raise err

        res = aiohu.models.JsonObj(**out)
        if not res.ok:
            raise RuntimeError(f"response is not ok: {res.status=}")

        print(repr(res))
        print(res.json)


if __name__ == "__main__":
    asyncio.run(main())
