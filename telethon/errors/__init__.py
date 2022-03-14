"""
This module holds all the base and automatically generated errors that the
Telegram API has. See telethon_generator/errors.json for more.
"""
import re

from .common import (
    ReadCancelledError, TypeNotFoundError, InvalidChecksumError,  # noqa: F401
    InvalidBufferError, SecurityError, CdnFileTamperedError,  # noqa: F401
    AlreadyInConversationError, BadMessageError, MultiError  # noqa: F401
)

from .rpcbaseerrors import *  # noqa: F403
from .rpcbaseerrors import _mk_error_type
from .rpcerrorlist import *  # noqa: F403


def __getattr__(name):
    return _mk_error_type(name=name)


def rpc_message_to_error(rpc_error, request):
    """
    Converts a Telegram's RPC Error to a Python error.

    :param rpc_error: the RpcError instance.
    :param request: the request that caused this error.
    :return: the RPCError as a Python exception that represents this error.
    """
    # Try to get the error by direct look-up, otherwise regex
    # Case-insensitive, for things like "timeout" which don't conform.
    cls = rpc_errors_dict.get(rpc_error.error_message.upper(), None)  # noqa: F405
    if cls:
        return cls(request=request)

    for msg_regex, cls in rpc_errors_re:  # noqa: F405
        m = re.match(msg_regex, rpc_error.error_message)
        if m:
            capture = int(m.group(1)) if m.groups() else None
            return cls(request=request, capture=capture)

    # Some errors are negative:
    # * -500 for "No workers running",
    # * -503 for "Timeout"
    #
    # We treat them as if they were positive, so -500 will be treated
    # as a `ServerError`, etc.
    cls = base_errors.get(abs(rpc_error.error_code), RPCError)  # noqa: F405
    return cls(request=request, message=rpc_error.error_message,
               code=rpc_error.error_code)
