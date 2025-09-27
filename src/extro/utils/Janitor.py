from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from extro.shared.types import EmptyFunction, Destroyable


class Janitor:
    """
    Utility class for managing and cleaning up resources.

    This class helps track objects or functions that need to be destroyed, disconnected, or otherwise cleaned up when they are no longer in use.
    """

    __slots__ = ("_managed",)

    _managed: "list[list[EmptyFunction]]"

    def __init__(self):
        self._managed = []

    def destroy(self):
        """Destroy the Janitor and clean up all managed resources."""
        self.cleanup()

    def add(self, instance: "Destroyable | EmptyFunction", *args):
        """
        Add a resource to be managed by the Janitor.

        Example
        -------
        >>> janitor = Janitor()
        >>> janitor.add(some_signal.disconnect, connection_id)
        >>> janitor.add(file_handle.close)
        """
        destroy_method: "EmptyFunction | None" = getattr(instance, "destroy", None)

        if callable(destroy_method):
            self._managed.append([destroy_method, *args])
        elif callable(instance):
            self._managed.append([instance, *args])

    def remove(self, instance: "Destroyable | EmptyFunction"):
        """Remove a managed resource from the Janitor without cleaning it up."""
        destroy_method: "EmptyFunction | None" = getattr(instance, "destroy", None)

        for index, [method, *_] in enumerate(self._managed):
            if method == destroy_method or method == instance:
                self._managed.pop(index)
                break

    def cleanup(self):
        """Calls all managed cleanup methods and clears the managed list."""
        for [method, *args] in list(self._managed):
            method(*args)

        self._managed.clear()
