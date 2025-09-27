from typing import TYPE_CHECKING

from extro.internal.services import Identity
import extro.Console as Console

if TYPE_CHECKING:
    from extro.shared.types import EmptyFunction


class Signal:
    """
    A simple signal/slot (observer) implementation for event handling.

    Subscribers can connect callback functions, which will be called
    whenever the signal is fired.

    Example
    -------
    >>> def on_event(value):
    ...     print("Event received:", value)
    ...
    >>> signal = Signal()
    >>> signal.connect(on_event)
    >>> signal.fire(42)
    Event received: 42
    """

    __slots__ = ("_is_active", "_subscribers")

    _is_active: bool
    _subscribers: dict[str, "EmptyFunction"]

    def __init__(self):
        self._is_active = True
        self._subscribers = {}

    def destroy(self):
        self._is_active = False
        self.disconnect_all()

    def connect(self, callback: "EmptyFunction") -> str:
        """
        Connect a callback function to the signal.

        The callback will be invoked when the signal is fired.
        """
        if not self._is_active:
            Console.log("Cannot connect to a destroyed signal", Console.LogType.WARNING)
            return ""

        connection_id = Identity.generate_id(5, "sig_")
        self._subscribers[connection_id] = callback
        return connection_id

    def disconnect(self, connection_id: str):
        """Disconnect a subscriber from the signal."""
        if connection_id not in self._subscribers:
            Console.log(
                f"{connection_id} is not a subscriber",
                Console.LogType.WARNING,
            )
            return

        self._subscribers.pop(connection_id, None)

    def disconnect_all(self):
        """Remove all subscribers from the signal."""
        self._subscribers.clear()

    def fire(self, *args):
        """Invoke all connected callbacks with the given arguments."""
        if not self._is_active or len(self._subscribers) == 0:
            return

        for subscriber in list(self._subscribers.values()):
            # The goal is to ensure one failing subscriber doesn't affect others
            try:
                subscriber(*args)
            except Exception as error:
                Console.log(
                    f"{subscriber.__name__, subscriber.__code__.co_firstlineno}: {error}",
                    Console.LogType.ERROR,
                )
