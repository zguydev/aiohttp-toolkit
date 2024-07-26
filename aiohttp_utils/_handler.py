from typing import Any, Optional, Literal, Callable, Awaitable

import yarl
import aiohttp


class RequestHandler:
    @staticmethod
    def _prepare_request(
        session: aiohttp.ClientSession,
        method: str,
        url: yarl.URL,
        params: dict[str, str]={},
        headers: dict[str, str]={},
        cookies: dict[str, str]={},
        data: Optional[bytes]=None,
        timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=30),
        **kwargs,
    ) -> aiohttp.client._RequestContextManager:
        r = session.request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            data=data,
            timeout=timeout,
            **kwargs,
        )
        return r

    @staticmethod
    async def _process_request(
        client_context: aiohttp.client._RequestContextManager,
        handler_callback: Callable[
            [Any], Awaitable[tuple[dict[str, Any], Optional[Exception]]]],
        **kwargs,
    ) -> tuple[
        dict[str, Any],
        Optional[Exception],
    ]:
        try:
            async with client_context as client_response:
                out, err = await handler_callback(
                    client_response,
                    **kwargs,
                )

                if err:
                    return {}, err

                return out, None

        except aiohttp.ClientError as err:
            return {}, err

    @staticmethod
    async def request(
        session: aiohttp.ClientSession,
        handler_callback: Callable[
            [Any], Awaitable[tuple[dict[str, Any], Optional[Exception]]]],
        handler_callback_kwargs: dict[str, Any],
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: yarl.URL,
        params: dict[str, str]={},
        headers: dict[str, str]={},
        cookies: dict[str, str]={},
        data: Optional[bytes]=None,
        timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=30),
        **kwargs,
    ) -> tuple[
        dict[str, Any],
        Optional[Exception],
    ]:
        client_context = RequestHandler._prepare_request(
            session=session,
            method=method,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            data=data,
            timeout=timeout,
            **kwargs,
        )

        out, err = await RequestHandler._process_request(
            client_context=client_context,
            handler_callback=handler_callback,
            **handler_callback_kwargs,
        )
        return out, err
