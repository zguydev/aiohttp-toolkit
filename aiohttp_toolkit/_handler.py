from typing import Any, Optional, Union, Literal, Callable, Awaitable, Iterable, Mapping
import types
import ssl
from http.cookies import BaseCookie

import yarl
import aiohttp
import multidict

from .types import (
    ResponseCbOut,
    CbBuilderOut,
)


__all__ = ("RequestHandler", "CallbackBuilder")


class RequestHandler:
    """
    A class for executing HTTP requests using `aiohttp` and handling the
    response via a callback.

    The `RequestHandler` class provides a static method to perform HTTP
    requests with various configurations, handle the response via a callback
    function, and return the processed data along with any exceptions in a
    Golang-style return format.

    Methods:
        `request` method performs an HTTP request, processes the response
        with a callback, and returns the handled data along with any
        exceptions.
    """

    @staticmethod
    def _prepare_request(
        session: aiohttp.ClientSession,
        *,
        method: str,
        url: yarl.URL,
        params: dict[str, str] = {},
        data: Optional[Union[bytes, Any]] = None,
        json: Optional[Any] = None,
        cookies: Optional[Union[dict[str, str], BaseCookie[str]]] = None,
        headers: Optional[Mapping[Union[str, multidict.istr], str]] = None,
        skip_auto_headers: Optional[Iterable[str]] = None,
        auth: Optional[aiohttp.BasicAuth] = None,
        allow_redirects: bool = True,
        max_redirects: int = 10,
        compress: Optional[str] = None,
        chunked: Optional[bool] = None,
        expect100: bool = False,
        raise_for_status: Optional[bool] = None,
        read_until_eof: bool = True,
        proxy: Optional[yarl.URL] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        timeout: Optional[aiohttp.ClientTimeout] = None,
        ssl: Union[bool, ssl.SSLContext, aiohttp.Fingerprint] = True,
        server_hostname: Optional[str] = None,
        proxy_headers: Optional[dict[str, str]] = None,
        trace_request_ctx: Optional[types.SimpleNamespace] = None,
        read_bufsize: Optional[int] = None,
        auto_decompress: Optional[bool] = None,
        max_line_size: Optional[int] = None,
        max_field_size: Optional[int] = None,
        verify_ssl: Optional[bool] = None,
        fingerprint: Optional[bytes] = None,
        ssl_context: Optional[ssl.SSLContext] = None,
    ) -> aiohttp.client._RequestContextManager:
        timeout_value = timeout if timeout is not None else aiohttp.helpers.sentinel

        r = session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            cookies=cookies,
            headers=headers,
            skip_auto_headers=skip_auto_headers,
            auth=auth,
            allow_redirects=allow_redirects,
            max_redirects=max_redirects,
            compress=compress,
            chunked=chunked,
            expect100=expect100,
            raise_for_status=raise_for_status,
            read_until_eof=read_until_eof,
            proxy=proxy,
            proxy_auth=proxy_auth,
            timeout=timeout_value,  # ! timeout_value is used instead of timeout
            ssl=ssl,
            server_hostname=server_hostname,
            proxy_headers=proxy_headers,
            trace_request_ctx=trace_request_ctx,
            read_bufsize=read_bufsize,
            auto_decompress=auto_decompress,
            max_line_size=max_line_size,
            max_field_size=max_field_size,
            verify_ssl=verify_ssl, # type: ignore Deprecated since version 3.0
            fingerprint=fingerprint, # type: ignore Deprecated since version 3.0
            ssl_context=ssl_context, # type: ignore Deprecated since version 3.0
        )
        return r

    @staticmethod
    async def _process_request(
        request_context: aiohttp.client._RequestContextManager,
        response_callback: Callable[..., Awaitable[ResponseCbOut]],
        **kwargs,
    ) -> tuple[dict[str, Any], Optional[Exception]]:
        try:
            async with request_context as client_response:
                out, err = await response_callback(
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
        response_callback: Callable[..., Awaitable[ResponseCbOut]],
        response_callback_kwargs: dict[str, Any],
        *,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: yarl.URL,
        params: dict[str, str] = {},
        data: Optional[Union[bytes, Any]] = None,
        json: Optional[Any] = None,
        cookies: Optional[Union[dict[str, str], BaseCookie[str]]] = None,
        headers: Optional[Mapping[Union[str, multidict.istr], str]] = None,
        allow_redirects: bool = True,
        max_redirects: int = 10,
        proxy: Optional[yarl.URL] = None,
        timeout: Optional[aiohttp.ClientTimeout] = None,
        **kwargs,
    ) -> tuple[dict[str, Any], Optional[Exception]]:
        """
        Perform an HTTP request with handling the response with callback
        and returning handled data, while also using Golang-style return
        exception.

        Args:
            **kwargs: Passed to `aiohttp.ClientSession.request`
            session: Interface for making HTTP requests
            response_callback: Response callback that is being called after response (if request was successful)
            response_callback_kwargs: Kwargs that are passed to response callback
            method: HTTP method
            url: Request URL
            params: Sent as parameters in the query string of the new request. Ignored for subsequent redirected requests (optional). Defaults to `{}`.
            data: The data to send in the body of the request. This can be a FormData object or anything that can be passed into FormData, e.g. a dictionary, bytes, or file-like object. Defaults to `None`.
            json: Any json compatible python object. json and data parameters could not be used at the same time. Defaults to `None`.
            cookies: HTTP Cookies to send with the request. Global session cookies and the explicitly set cookies will be merged when sending the request. Defaults to `None`.
            headers: HTTP Headers to send with the request. Defaults to `None`.
            allow_redirects: If set to False, do not follow redirects. Defaults to `True`.
            max_redirects: Maximum number of redirects to follow. Defaults to `10`.
            proxy: Proxy URL. Defaults to `None`.
            timeout: Override the session's timeout. Defaults to `None`.

        Returns:
            tuple[dict[str, Any], Optional[Exception]]: tuple with handled data
            and optional exception.\n
            If the exception is `None` it is recommended to apply dataclass to
            get a typed response:

            ```python
            import aiohttp_utils as aiohu


            callback = aiohu.callbacks.json

            out, err = aiohu.RequestHandler.request(..., response_callback=callback)
            if err:
                raise err

            res = aiohu.models.JsonObj(out)
            ```
        """

        client_context = RequestHandler._prepare_request(
            session=session,
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            cookies=cookies,
            headers=headers,
            allow_redirects=allow_redirects,
            max_redirects=max_redirects,
            proxy=proxy,
            timeout=timeout,
            **kwargs,
        )

        out, err = await RequestHandler._process_request(
            request_context=client_context,
            response_callback=response_callback,
            **response_callback_kwargs,
        )
        return out, err


class CallbackBuilder:
    """
    A utility class for building HTTP response callback handlers that can
    sequentially process data using a chain of handlers.

    Methods:
        `build` method returns a callback function that will process an
        `aiohttp.ClientResponse` object using the provided handlers.

        `develop` method returns a callback function that will process an
        `aiohttp.ClientResponse` object using the provided handlers, developing
        the built callback with new handlers.
    """

    @staticmethod
    def build(
        *handlers: Callable[
            [dict[str, Any], aiohttp.ClientResponse],
            Awaitable[CbBuilderOut],
        ],
    ) -> Callable[..., Awaitable[ResponseCbOut]]:
        """
        Build a response callback function from a sequence of asynchronous
        handlers.

        Each handler is an asynchronous function that processes a data
        dictionary and an `aiohttp.ClientResponse` object. The handlers are
        executed in the order they are provided. If any handler returns an
        error, the process is terminated, and the error is returned, while
        also return a built prior to that handler dictionary.

        Args:
            *handlers: A variable number of asynchronous handler functions,
            each taking a dictionary and an `aiohttp.ClientResponse` object
            as input and returning a modified dictionary and an error object.

        Returns:
            Callable[..., Awaitable[ResponseCbOut]]: An asynchronous callback
            function that processes the HTTP response and additional keyword
            arguments.
        """

        async def response_callback(
            cr: aiohttp.ClientResponse,
            **kwargs,
        ) -> ResponseCbOut:
            nonlocal handlers

            out: dict[str, Any] = {}

            for handler in handlers:
                out, err = await handler(out, cr, **kwargs)
                if err:
                    return out, err

            return out, None

        return response_callback

    @staticmethod
    def develop(
        built: Callable[..., Awaitable[ResponseCbOut]],
        *handlers: Callable[
            [dict[str, Any], aiohttp.ClientResponse],
            Awaitable[CbBuilderOut],
        ],
    ) -> Callable[..., Awaitable[ResponseCbOut]]:
        """
        Enhance an existing response callback with additional asynchronous
        handlers, allowing further processing of the data.

        The `develop` method takes an existing callback function (`built`) and
        appends additional handlers to it. The returned callback first executes
        the original callback, and then processes the output using the new
        handlers sequentially.

        Args:
            built: An existing asynchronous callback function that returns a
            dictionary and an error object after processing an
            `aiohttp.ClientResponse`.
            *handlers: Additional asynchronous handler functions that take a
            dictionary and an `aiohttp.ClientResponse` object as input, returning
            a modified dictionary and an error object.

        Returns:
            Callable[..., Awaitable[ResponseCbOut]]: An asynchronous callback
            function that first invokes the provided `built` callback and then
            processes its output with the additional handlers.
        """

        async def response_callback(
            cr: aiohttp.ClientResponse,
            **kwargs,
        ) -> ResponseCbOut:
            nonlocal built, handlers

            out, err = await built(cr, **kwargs)
            if err:
                return out, err

            for handler in handlers:
                out, err = await handler(out, cr, **kwargs)
                if err:
                    return out, err

            return out, None

        return response_callback
