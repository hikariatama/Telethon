from .common import EventBuilder
from .. import utils


class Raw(EventBuilder):
    """
    Raw events are not actual events. Instead, they are the raw
    :tl:`Update` object that Telegram sends. You normally shouldn't
    need these.

    Args:
        types (`list` | `tuple` | `type`, optional):
            The type or types that the :tl:`Update` instance must be.
            Equivalent to ``if not isinstance(update, types): return``.

    Example
        .. code-block:: python

            from telethon import events

            @client.on(events.Raw)
            async def handler(update):
                # Print all incoming updates
                print(update.stringify())
    """

    def __init__(self, types=None, *, func=None):
        super().__init__(func=func)
        if not types:
            self.types = None
        elif not utils.is_list_like(types):
            if not isinstance(types, type):
                raise TypeError("Invalid input type given: {}".format(types))

            self.types = types
        elif all(isinstance(x, type) for x in types):
            self.types = tuple(types)
        else:
            raise TypeError("Invalid input types given: {}".format(types))

    async def resolve(self, client):
        self.resolved = True

    @classmethod
    def build(cls, update, others=None, self_id=None):
        return update

    def filter(self, event):
        if not self.types or isinstance(event, self.types):
            return self.func(event) if self.func else event
