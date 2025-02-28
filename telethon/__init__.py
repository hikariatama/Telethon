from .client.telegramclient import TelegramClient
from .network import connection
from .tl import types, functions, custom
from .tl.custom import Button
from .tl import patched as _  # noqa: F401
from . import version, events, utils, errors

__version__ = version.__version__

__all__ = [
    "TelegramClient",
    "Button",
    "types",
    "functions",
    "custom",
    "errors",
    "events",
    "utils",
    "connection",
]
