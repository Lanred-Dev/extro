from typing import TYPE_CHECKING

from src.internal.Console import Console, LogType
from src.internal.InstanceHandler import InstanceHandler
from src.internal.components.Signal import Signal
from src.internal.components.Janitor import Janitor
from src.internal.components.DirtyUpdater import DirtyUpdater
from src.values.Vector2 import Vector2
from src.values.Color import Color
from src.shared_types import EmptyFunction

if TYPE_CHECKING:
    from instances.Scene import Scene


class Instance(DirtyUpdater):
    """
    Base class representing a renderable object in a scene.

    Instances can be positioned, resized, colored, and parented
    to other instances. They automatically handle cleanup when
    destroyed.
    """

    id: str
    size: Vector2
    position: Vector2
    actual_position: Vector2
    anchor: Vector2
    color: Color

    scene: "Scene | None"
    parent: "Instance | None"
    __on_parent_destroy_connection: str | None
    __on_parent_update_connection: str | None

    on_update: Signal
    on_destroy: Signal
    janitor: Janitor

    def __init__(self):
        super().__init__()
        self.id: str = InstanceHandler.create_instance_id()
        self.__on_parent_destroy_connection = None
        self.__on_parent_update_connection = None
        self.scene = None
        self.parent = None

        self.on_destroy = Signal()
        self.on_update = Signal()
        self.janitor = Janitor()
        self.janitor.add(self.on_update)
        self.janitor.add(self.on_destroy.fire)
        self.janitor.add(self.on_destroy)

        self.anchor = Vector2(0, 0)
        self.size = Vector2(100, 100)
        self.color = Color(255, 255, 255)
        self.set_position(Vector2(0, 0))

        InstanceHandler.register_instance(self)
        self.janitor.add(InstanceHandler.unregister_instance, self)

    def destroy(self):
        self.janitor.destroy()

    def parent_to(self, parent: "Instance | str | None"):
        """
        Set this instance's parent.

        Args:
            parent: Either an `Instance`, an ID string, or None.
        """
        self.__disconnect_parent_connections()

        if isinstance(parent, str):
            parent_cls = InstanceHandler.instances[parent]
        elif isinstance(parent, Instance):
            parent_cls = parent
        else:
            parent_cls = None

        if parent_cls is None:
            self.parent = None
            return
        elif self.scene is None and parent_cls.scene is not None:
            parent_cls.scene.add_instance(self)
            Console.log(
                f"{self.id} was added to {parent_cls.scene.id} because of parent"
            )
        elif (
            self.scene is not None
            and parent_cls.scene is not None
            and self.scene.id != parent_cls.scene.id
        ):
            Console.log(
                f"{self.id} could not be parented to {parent_cls.id} "
                f"because they are in different scenes",
                LogType.ERROR,
            )
            return

        self.parent = parent_cls
        self.__on_parent_destroy_connection = parent_cls.on_update.connect(
            self._on_parent_update
        )
        self.__on_parent_destroy_connection = parent_cls.on_destroy.connect(
            self.destroy
        )

    def set_anchor(self, anchor: Vector2):
        """
        Set the anchor point of this instance.

        The anchor determines the pivot for positioning and rotation.
        """
        self.anchor = anchor
        self._apply_anchor_to_position()
        self.__adjust_position_based_on_parent()

    def set_position(self, position: Vector2):
        """
        Set the absolute position of this instance.

        Updates the instance's position directly and applies its anchor offset.
        """
        self.position = position
        self._apply_anchor_to_position()
        self.__adjust_position_based_on_parent()
        self.on_update.fire()

    def set_relative_position(self, position: Vector2):
        """
        Set the position of this instance relative to its parent.

        The position is calculated based on the parent's bounding box
        and the relative coordinates provided.
        """
        if self.parent is None:
            Console.log(
                "The instance must have a parent for `set_relative_position` to work",
                LogType.WARNING,
            )
            return

        [parent_x, parent_y, parent_width, parent_height] = self.parent.get_bounding()
        position.x = parent_x + (parent_width * position.x)
        position.y = parent_y + (parent_height * position.y)
        self.set_position(position)

    def set_relative_size(self, size: Vector2):
        """
        Set the size relative to the parent instance.

        The size is calculated based on the parent's bounding box.
        """
        if self.parent is None:
            Console.log(
                "The instance must have a parent for `set_relative_size` to work",
                LogType.WARNING,
            )
            return

        [_, _, parent_width, parent_height] = self.parent.get_bounding()
        size.x = parent_width * size.x
        size.y = parent_height * size.y
        self.set_size(size)

    def set_size(self, size: Vector2):
        self.size = size
        self._apply_anchor_to_position()
        self.on_update.fire()

    def set_color(self, color: Color):
        """Set the instance's display color."""
        self.color = color
        self.on_update.fire()

    def get_bounding(self) -> tuple[float, float, float, float]:
        """
        Get the bounding rectangle of this instance.

        Returns:
            tuple[float, float, float, float]: (x, y, width, height)
        """
        return (
            self.actual_position.x,
            self.actual_position.y,
            self.size.x,
            self.size.y,
        )

    def mark_dirty(self, callback: EmptyFunction):
        super().mark_dirty(callback)
        InstanceHandler.queue_dirty_instance_for_update(self)

    def _on_parent_update(self):
        self._apply_anchor_to_position()
        self.__adjust_position_based_on_parent()

    def _apply_anchor_to_position(self):
        """Adjust the actual position according to the anchor point."""
        self.actual_position = self.position.copy()
        self.actual_position.x -= self.size.x * self.anchor.x
        self.actual_position.y -= self.size.y * self.anchor.y

    def __adjust_position_based_on_parent(self):
        """Offset the actual position based on the parent's position."""
        if self.parent is None:
            return

        self.actual_position += self.parent.actual_position

    def __disconnect_parent_connections(self):
        """Disconnect from the parent's signals."""
        if self.parent is None:
            return

        if self.__on_parent_destroy_connection is not None:
            self.parent.on_destroy.disconnect(self.__on_parent_destroy_connection)
            self.__on_parent_destroy_connection = None

        if self.__on_parent_update_connection is not None:
            self.parent.on_update.disconnect(self.__on_parent_update_connection)
            self.__on_parent_update_connection = None
