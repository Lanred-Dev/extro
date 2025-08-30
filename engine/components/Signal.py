from engine.utils.id import generate_id
import typing
from engine.utils.types import BasicFunction
from engine.Console import console, LogType


class Signal:
    """
    A simple signal/slot (observer) implementation for event handling.

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

    def __init__(self):
        self.__is_active: bool = True
        self.__subscribers: dict[str, BasicFunction] = {}

    def destroy(self):
        """Destroy the signal."""

        self.__is_active = False
        self.disconnect_all()

    def connect(self, callback: BasicFunction) -> str:
        """Connect a function or method to the signal so it is called when fired.

        Returns
        -------
        str
            The ID of the connection.
        """

        if not self.__is_active:
            console.log(
                "Tried to connect to a signal that has been destroyed.",
                LogType.WARNING,
            )
            return ""

        id = generate_id(10)
        self.__subscribers[id] = callback
        return id

    def disconnect(self, id: str):
        """Remove a connection from the signal."""

        self.__subscribers.pop(id, None)

    def disconnect_all(self):
        """Remove all connections from the signal."""

        self.__subscribers = {}

    def fire(self, *args: typing.Any, **kwargs: typing.Any):
        """Invoke all connected callbacks with the given arguments."""

        if not self.__is_active:
            console.log(
                "Tried to fire a signal that has been destroyed.", LogType.WARNING
            )
            return

        # No need to fire if there is no subscribers
        if len(self.__subscribers) == 0:
            return

        for subscriber in list(self.__subscribers.values()):
            subscriber(*args, **kwargs)
