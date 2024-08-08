from ._handler import CallbackBuilder as _cbuilder
from . import callback_builders as _cbb


__all__ = (
    "status",
    "info",
    "read",
    "text",
    "json",
)


status = _cbuilder.build(
    _cbb.status,
)

info = _cbuilder.build(
    _cbb.status,
    _cbb.headers,
    _cbb.cookies,
)

read = _cbuilder.develop(
    info,
    _cbb.read,
)

text = _cbuilder.build(
    info,
    _cbb.text,
)

json = _cbuilder.build(
    info,
    _cbb.json,
)
