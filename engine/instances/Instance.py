from engine.utils.types import RelativeCoord, RelativeCoords, BasicInstance
from engine.components import Signal, Janitor
from engine import engine
from engine.Console import console, LogType
import pygame
import typing
from enum import Enum

ParentInstance = typing.Union[str, BasicInstance, None]


class RenderUpdateType(Enum):
    COLOR = 0
    POSITION = 1
    SIZE = 2


class Instance:
    """
    Base class for all game instances in the engine.

    Provides fundamental functionality such as position, unique ID, and integration with the engine's update loop. Other game instances should inherit from this class to gain these base features.

    Example
    -------
    inst = Instance()
    inst.position = pygame.Vector2(100, 200)
    """

    def __init__(self):
        self.id = engine.create_instance_id()
        self.zindex: int = 0
        self.size: pygame.Vector2 = pygame.Vector2(0, 0)
        self.position: pygame.Vector2 = pygame.Vector2(0, 0)
        self.actual_position: pygame.Vector2 = pygame.Vector2(0, 0)
        self.anchor: RelativeCoords = (0, 0)
        self.color: pygame.Color = pygame.Color(255, 255, 255)
        self.is_active: bool = True
        self.janitor = Janitor()
        self.janitor.add(self.__disconnect_parent_destroy_connection)

        self.parent: Instance | None = None
        self.__on_parent_destroy_connection: str | None = None

        self.on_destroy: Signal = Signal()
        self.janitor.add(self.on_destroy.fire)
        self.janitor.add(self.on_destroy)

    def init(self):
        engine.register_instance(self.id, self)
        self.janitor.add(engine.unregister_instance, self.id)

    def destroy(self):
        """Destroy the instance and emit its on_destroy signal."""
        self.janitor.destroy()

    def set_zindex(self, zindex: int):
        self.zindex = zindex
        engine.update_instance_render_list()

    def parent_to(self, instance: ParentInstance):
        """
        Set the parent instance of this instance.

        If a parent id is provided, the instance is parented to the corresponding instance from the engine's object registry. If None is provided, the instance will have no parent.
        """

        self.__disconnect_parent_destroy_connection()

        if isinstance(instance, BasicInstance) and instance.id in engine.instances:
            # Assume that this is a valid instance if it has an ID
            self.parent = instance  # type: ignore
        elif isinstance(instance, str) and instance in engine.instances:
            self.parent = engine.instances[instance]
        elif instance is None:
            self.parent = None
        else:
            console.log("Invalid parent instance passed to `parent_to`.", LogType.ERROR)
            return

        if self.parent is not None:
            self.__on_parent_destroy_connection = self.parent.on_destroy.connect(
                self.destroy
            )

    def set_global_position(self, x: float, y: float):
        """
        Set the absolute position of this instance in the game world.

        This updates the instance's position directly and applies its anchor offset.
        """
        self.position.x = x
        self.position.y = y
        self.update_render(RenderUpdateType.POSITION)

    def set_relative_position(self, x: RelativeCoord, y: RelativeCoord):
        """
        Set the position of this instance relative to its parent.

        The position is calculated based on the parent's bounding box and the relative coordinates provided. No action is taken if the instance has no parent.
        """
        if self.parent is None:
            console.log(
                "The instance must have a parent for `set_relative_position` to work",
                LogType.WARNING,
            )
            return

        [parent_x, parent_y, parent_width, parent_height] = self.parent.get_bounding()
        self.position.x = parent_x + (parent_width * x)
        self.position.y = parent_y + (parent_height * y)
        self.update_render(RenderUpdateType.POSITION)

    def set_global_size(self, x: float, y: float):
        self.size.x = x
        self.size.y = y
        self.update_render(RenderUpdateType.SIZE)

    def set_relative_size(self, x: RelativeCoord, y: RelativeCoord):
        if self.parent is None:
            console.log(
                "The instance must have a parent for `set_relative_size` to work",
                LogType.WARNING,
            )
            return

        [_parent_x, _parent_y, parent_width, parent_height] = self.parent.get_bounding()
        self.size.x = parent_width * x
        self.size.y = parent_height * y
        self.update_render(RenderUpdateType.SIZE)

    def set_color(self, r: int = 0, g: int = 0, b: int = 0, a: int = 255):
        self.color.r = r
        self.color.g = g
        self.color.b = b
        self.color.a = a
        self.update_render(RenderUpdateType.COLOR)

    def get_bounding(self) -> tuple[float, float, float, float]:
        """
        Get the bounding rectangle of this instance.

        Returns
        -------
        tuple[float, float, float, float]
            A tuple containing (x, y, width, height) representing the instance's position and size in world coordinates.
        """
        return (
            self.actual_position.x,
            self.actual_position.y,
            self.size.x,
            self.size.y,
        )

    def update_render(self, type: RenderUpdateType):
        self.update_size()
        self.update_position()

    def update_size(self):
        pass

    def update_position(self):
        """Update the instance's position and apply anchor adjustments."""
        self.__apply_anchor_to_position()
        self.__adjust_for_parent_position()

    def predraw(self):
        # Position will only change this way if it has a parent
        if self.parent is not None:
            self.update_position()

    def __apply_anchor_to_position(self):
        """Adjust the actual position of the instance according to its anchor."""
        self.actual_position = self.position.copy()
        self.actual_position.x -= self.size.x * self.anchor[0]
        self.actual_position.y -= self.size.y * self.anchor[1]

    def __adjust_for_parent_position(self):
        """Offset the position based on the parent to maintain relative positioning."""
        if self.parent is None:
            return

        self.actual_position += self.parent.actual_position

    def __disconnect_parent_destroy_connection(self):
        """Disconnects the old parent connection."""
        if self.__on_parent_destroy_connection is None or self.parent is None:
            return

        self.parent.on_destroy.disconnect(self.__on_parent_destroy_connection)
        self.__on_parent_destroy_connection = None
