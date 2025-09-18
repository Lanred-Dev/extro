from typing import TYPE_CHECKING
import src.internal.services.IdentityService as IdentityService

if TYPE_CHECKING:
    from src.internal.shared_types import EmptyFunction


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

    _is_active: bool
    _subscribers: dict[str, "EmptyFunction"]

    def __init__(self):
        self._is_active = True
        self._subscribers = {}

    def destroy(self):
        """Destroy the signal and remove all subscribers."""
        self._is_active = False
        self.disconnect_all()

    def connect(self, callback: "EmptyFunction") -> str:
        """
        Connect a callback function to the signal.

        The callback will be invoked when the signal is fired.

        Args:
            callback: A function or method to be executed.

        Returns:
            str: A unique ID for the connection. Returns an empty string
                 if the signal has been destroyed.
        """
        if not self._is_active:
            return ""

        connection_id = IdentityService.generate_id(5, "sig_")
        self._subscribers[connection_id] = callback
        return connection_id

    def disconnect(self, connection_id: str):
        """
        Disconnect a callback from the signal.

        Args:
            connection_id: The unique ID of the subscriber to remove.
        """
        self._subscribers.pop(connection_id, None)

    def disconnect_all(self):
        """Remove all subscribers from the signal."""
        self._subscribers.clear()

    def fire(self, *args):
        """
        Invoke all connected callbacks with the given arguments.

        Args:
            *args: Positional arguments passed to each callback.
            **kwargs: Keyword arguments passed to each callback.
        """
        if not self._is_active:
            return

        if not self._subscribers:
            return

        for subscriber in list(self._subscribers.values()):
            subscriber(*args)
