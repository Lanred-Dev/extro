import pyglet
from typing import List

from src.internal.IdentityHandler import generate_id
from src.internal.Console import Console, LogType
from src.internal.Renderer import Renderer
from src.instances.core.Instance import Instance
from src.internal.SceneHandler import SceneHandler
from src.internal.InstanceHandler import InstanceHandler


class Scene:
    """
    Represents a scene containing renderable instances.

    Handles instance addition/removal and maintains a render order
    based on instance z-index.
    """

    id: str
    zindex: int
    batch: pyglet.graphics.Batch
    __instances: List[str]

    def __init__(self, id: str = generate_id(prefix="s_")):
        """Initialize a new scene and register it with the SceneHandler."""
        self.id = id
        self.zindex = 0
        self.batch = pyglet.graphics.Batch()
        self.__instances = []
        SceneHandler.register_scene(self)

    def destroy(self):
        """Unregister the scene from the SceneHandler."""
        SceneHandler.unregister_scene(self)

    def add_instance(self, instance: Instance):
        """
        Add an instance to the scene.

        Args:
            instance: The Instance to add.

        Logs a warning if the instance is already part of a scene.
        """
        if instance.scene is not None:
            Console.log(
                f"{instance.id} is already part of scene {instance.scene.id}",
                LogType.WARNING,
            )
            return

        instance.scene = self
        self.__instances.append(instance.id)
        Console.log(f"{instance.id} was added to {self.id}")

        if callable(getattr(instance, "create_mesh", None)):
            instance.create_mesh()  # type: ignore

    def remove_instance(self, instance: Instance | str):
        """
        Remove an instance from the scene.

        Args:
            instance: The Instance object or its ID.

        Logs a warning if the instance does not exist in the scene.
        """
        if isinstance(instance, str):
            instance_id = instance
        else:
            instance_id = instance.id

        if instance_id not in self.__instances:
            Console.log(f"{instance_id} does not exist in {self.id}", LogType.WARNING)
            return

        self.__instances.remove(instance_id)
        Console.log(f"{instance_id} was removed from {self.id}")

    def set_zindex(self, zindex: int):
        """
        Set the z-index of the scene.

        Args:
            zindex: The new z-index value.

        Updates the renderer's scene render order.
        """
        self.zindex = zindex
        Renderer.update_render_order_list()
