from typing import Any
from src.shared_types import EmptyFunction
from src.internal.IdentityHandler import generate_id


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

    __is_active: bool
    __subscribers: dict[str, EmptyFunction]

    def __init__(self):
        self.__is_active = True
        self.__subscribers = {}

    def destroy(self):
        """Destroy the signal and remove all subscribers."""
        self.__is_active = False
        self.disconnect_all()

    def connect(self, callback: EmptyFunction) -> str:
        """
        Connect a callback function to the signal.

        The callback will be invoked when the signal is fired.

        Args:
            callback: A function or method to be executed.

        Returns:
            str: A unique ID for the connection. Returns an empty string
                 if the signal has been destroyed.
        """
        if not self.__is_active:
            return ""

        connection_id = generate_id(5, "sig_")
        self.__subscribers[connection_id] = callback
        return connection_id

    def disconnect(self, connection_id: str):
        """
        Disconnect a callback from the signal.

        Args:
            connection_id: The unique ID of the subscriber to remove.
        """
        self.__subscribers.pop(connection_id, None)

    def disconnect_all(self):
        """Remove all subscribers from the signal."""
        self.__subscribers.clear()

    def fire(self, *args: Any, **kwargs: Any):
        """
        Invoke all connected callbacks with the given arguments.

        Args:
            *args: Positional arguments passed to each callback.
            **kwargs: Keyword arguments passed to each callback.
        """
        if not self.__is_active:
            return

        if not self.__subscribers:
            return

        for subscriber in list(self.__subscribers.values()):
            subscriber(*args, **kwargs)
