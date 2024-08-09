from typing import Any
import dataclasses
import collections
import asyncio

import aiohttp
import yarl

import aiohttp_toolkit as aiohtk


class ResponseRejectedError(aiohttp.ClientResponseError):
    pass

    def __repr__(self) -> str:
        max_num = getattr(self, "max_num")
        return f"ResponseRejectedError(max_num={max_num})"


async def check_rejection(
    data: dict[str, Any],
    cr: aiohttp.ClientResponse,
    **kwargs,
) -> aiohtk.types.CbBuilderOut:
    max_num = max(data["json"])

    data |= dict(
        max_num=max_num,
    )

    if max_num > 800:
        err = ResponseRejectedError(
            request_info=cr.request_info,
            history=cr.history,
            status=cr.status,
            message="response was rejected",
            headers=cr.headers,
        )
        setattr(err, "max_num", max_num)

        return data, err

    return data, None


check_response = aiohtk.CallbackBuilder.develop(
    aiohtk.callbacks.json,
    aiohtk.builders.close,
    check_rejection,
)


@dataclasses.dataclass
class Checked(aiohtk.models.JsonList):
    max_num: int

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}({self.status} "
            f"max_num={self.max_num})>"
        )

    def __hash__(self) -> int:
        return self.max_num


async def main() -> None:
    url = yarl.URL("https://www.randomnumberapi.com/api/v1.0/random") % dict(
        minx=0,
        max=1000,
        count=5,
    )

    async with aiohttp.ClientSession() as session:
        requests = [
            aiohtk.RequestHandler.request(
                session=session,
                response_callback=check_response,
                response_callback_kwargs={},
                method="GET",
                url=url,
            )
            for _ in range(100)
        ]
        outs = await asyncio.gather(*requests)

        results = [err if err else Checked(**request) for request, err in outs]
        counter = collections.Counter(results)
        print(f"Results: {counter}")


if __name__ == "__main__":
    asyncio.run(main())
