from typing import Any
import dataclasses
import asyncio

import aiohttp
import yarl

import aiohttp_toolkit as aiohtk


async def set_url(
    data: dict[str, Any],
    cr: aiohttp.ClientResponse,
    **kwargs,
) -> aiohtk.types.CbBuilderOut:
    data |= dict(
        _url=cr.url,
    )

    return data, None

json_with_url = aiohtk.CallbackBuilder.develop(
    aiohtk.callbacks.json,
    set_url,
)


@dataclasses.dataclass
class JsonAnyWithUrl(aiohtk.models.JsonAny):
    _url: yarl.URL

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}({self.status} {self._url}): "
            "{}>".format(repr(self.headers).strip("<>"))
        )


async def main() -> None:
    url = yarl.URL("https://httpbin.dev/json")

    async with aiohttp.ClientSession() as session:
        out, err = await aiohtk.RequestHandler.request(
            session=session,
            response_callback=json_with_url,
            response_callback_kwargs={},
            method="GET",
            url=url,
        )
        if err:
            raise err

        res = JsonAnyWithUrl(**out)
        if not res.ok:
            raise RuntimeError(f"response is not ok: {res.status=}")

        print(repr(res))


if __name__ == "__main__":
    asyncio.run(main())
