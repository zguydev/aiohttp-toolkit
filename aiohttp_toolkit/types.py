from typing import Any, Optional


__all__ = ("CbBuilderOut", "ResponseCbOut")


CbBuilderOut = tuple[dict[str, Any], Optional[Exception]]
"""
Return type of callback builder.\n
Alias for `tuple[dict[str, Any], Optional[Exception]]`
"""

ResponseCbOut = tuple[dict[str, Any], Optional[Exception]]
"""
Return type of response callback.\n
Alias for `tuple[dict[str, Any], Optional[Exception]]`
"""
