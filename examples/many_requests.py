import asyncio
import time
import datetime
import collections

import aiohttp
import yarl

import aiohttp_utils as aiohu


async def main() -> None:
    url = yarl.URL("https://example.com")

    async with aiohttp.ClientSession() as session:
        start = time.perf_counter()

        requests = [
            aiohu.RequestHandler.request(
                session=session,
                response_callback=aiohu.callbacks.text,
                response_callback_kwargs={},
                method="GET",
                url=url,
            )
            for _ in range(1_000)
        ]
        outs = await asyncio.gather(*requests)

        results = [
            err if err else request["status"]
            for request, err in outs
        ]
        counter = collections.Counter(results)
        print(f"Results: {counter}")

        time_passed = datetime.timedelta(seconds=time.perf_counter() - start)
        print(f"Time passed: {time_passed}")


if __name__ == "__main__":
    asyncio.run(main())
