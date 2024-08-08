from ._handler import CallbackBuilder as _cbuilder
from . import callback_builders as _cbb


__all__ = (
    "status",
    "properties",
    "read",
    "text",
    "json",
)


status = _cbuilder.build(
    _cbb.status,
)
"""
`status` - return response status code and it's boolean representation

Returns:
    status (str): response status code
    ok (bool): response status code boolean representation.
    `True` if status is less than 400; otherwise, `False`.
"""

properties = _cbuilder.build(
    _cbb.status,
    _cbb.headers,
    _cbb.cookies,
)
"""
`properties` - return all property-like response fields: response status code,
it's boolean representation, headers and cookies

Returns:
    status (str): response status code
    ok (bool): response status code boolean representation.
    `True` if status is less than 400; otherwise, `False`.
    headers (CIMultiDictProxy[str]): inmutable case-insensitive multidict with
    HTTP response headers.
    cookies (http.cookies.SimpleCookie): container with HTTP response cookies.
"""

read = _cbuilder.develop(
    properties,
    _cbb.read,
)
"""
`read` - return response body `bytes` and all property-like response fields
(listed in `properties` response callback)

Returns:
    status (str): response status code
    ok (bool): response status code boolean representation.
    `True` if status is less than 400; otherwise, `False`.
    headers (CIMultiDictProxy[str]): inmutable case-insensitive multidict with
    HTTP response headers.
    cookies (http.cookies.SimpleCookie): container with HTTP response cookies.
    read (bytes): response body bytes
"""

text = _cbuilder.build(
    properties,
    _cbb.text,
)
"""
`text` - return response body decoded as `str` and all property-like response
fields (listed in `properties` response callback)

Arguments:
    text (**kwargs): kwargs to be unpacked as
    `aiohttp.ClientResponse.text(**kwargs)`

Returns:
    status (str): response status code
    ok (bool): response status code boolean representation.
    `True` if status is less than 400; otherwise, `False`.
    headers (CIMultiDictProxy[str]): inmutable case-insensitive multidict with
    HTTP response headers.
    cookies (http.cookies.SimpleCookie): container with HTTP response cookies.
    text (str): response body decoded
"""

json = _cbuilder.build(
    properties,
    _cbb.json,
)
"""
`json` - return response body with json, deserialized as a Python object, also
all property-like response fields (listed in `properties` response callback)

Arguments:
    json (**kwargs): kwargs to be unpacked as
    `aiohttp.ClientResponse.json(**kwargs)`
"""
