from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.internal.shared_types import EmptyFunction, Destroyable


class Janitor:
    """
    Utility class for managing and cleaning up resources.

    This class helps track objects or functions that need to be destroyed, disconnected, or otherwise cleaned up when they are no longer in use.
    """

    _managed: list[list["EmptyFunction"]]

    def __init__(self):
        self._managed = []

    def destroy(self):
        """Destroy the Janitor and clean up all managed resources."""
        self.cleanup()

    def add(self, instance: "Destroyable | EmptyFunction", *args):
        """
        Add a resource to be managed by the Janitor.

        Args:
            instance: A `Destroyable` object or callable function.
            *args: Optional arguments passed when the resource is cleaned up.

        Example:
            janitor = Janitor()
            janitor.add(some_signal.disconnect)
            janitor.add(file_handle.close)
        """
        destroy_method: "EmptyFunction | None" = getattr(instance, "destroy", None)

        if callable(destroy_method):
            self._managed.append([destroy_method, *args])
        elif callable(instance):
            self._managed.append([instance, *args])

    def cleanup(self):
        """
        Clean up all managed resources.

        Calls each stored cleanup method with its arguments,
        then clears the internal list.
        """
        for [method, *args] in list(self._managed):
            # Instances may be destroyed before the janitor is cleaned up, so we need to check if the method is callable
            if callable(method):
                method(*args)

        self._managed.clear()
