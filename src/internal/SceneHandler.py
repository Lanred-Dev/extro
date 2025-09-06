from typing import TYPE_CHECKING
from src.internal.Console import Console, LogType
from src.internal.Renderer import Renderer

if TYPE_CHECKING:
    from instances.Scene import Scene


class SceneHandlerCls:
    """Manages registration and retrieval of scenes."""

    __scenes: dict[str, "Scene"]

    def __init__(self):
        self.__scenes = {}

    def register_scene(self, scene: "Scene"):
        """Register a scene and add it as a render target."""
        self.__scenes[scene.id] = scene
        Console.log(f"Registered scene {scene.id}")
        Renderer.add_render_target(scene)

    def unregister_scene(self, scene: "Scene | str"):
        """Unregister a scene and remove it from render targets."""
        if isinstance(scene, str):
            scene_id = scene
        elif isinstance(scene, Scene):
            scene_id = scene.id

        if scene_id not in self.__scenes:
            Console.log(f"{scene_id} is not an scene", LogType.WARNING)
            return

        self.__scenes.pop(scene_id, None)
        Console.log(f"{scene_id} is no longer an scene")
        Renderer.remove_render_target(scene)

    def get_scene_with_id(self, id: str) -> "Scene | None":
        """Retrieve a registered scene by its ID."""
        return self.__scenes.get(id)


SceneHandler = SceneHandlerCls()
__all__ = ["SceneHandler"]
