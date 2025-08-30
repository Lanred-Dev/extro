from engine.utils.types import BasicFunction, Destroyable
import typing

JanitorInstance = typing.Union[Destroyable, BasicFunction]


class Janitor:
    """Utility class for managing and cleaning up deletable instances."""

    def __init__(self):
        self.__managed: list[list[BasicFunction]] = []

    def destroy(self):
        """Destroy the Janitor and clean up all managed instances."""
        self.cleanup()

    def add(self, instance: JanitorInstance, *args: typing.Any):
        """Add a deletable instance to be managed by the Janitor."""
        if isinstance(instance, Destroyable):
            self.__managed.append([instance.destroy, *args])
        elif callable(instance):
            self.__managed.append([instance, *args])

    def cleanup(self):
        """Delete all managed instances and connections and clear the list."""
        for [method, *args] in list(self.__managed):
            method(*args)

        self.__managed = []
