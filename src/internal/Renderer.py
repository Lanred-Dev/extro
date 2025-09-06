from typing import TYPE_CHECKING, List, Dict

from src.internal.Window import Window
from src.internal.Console import Console, LogType

if TYPE_CHECKING:
    from instances.Scene import Scene


class RendererCls:
    """
    Central renderer manager for handling scenes and rendering order.

    Keeps track of active render targets (scenes) and ensures they
    are rendered in the correct order based on z-index.
    """

    __render_targets: Dict[str, "Scene"]
    __render_order: List[str]

    def __init__(self):
        self.__render_targets = {}
        self.__render_order = []

    def add_render_target(self, scene: "Scene"):
        """
        Add a scene as a render target.

        Args:
            scene: The scene to register for rendering.
        """
        self.__render_targets[scene.id] = scene
        Console.log(f"{scene.id} is now a render target")
        self.update_render_order_list()

    def remove_render_target(self, scene: "Scene | str"):
        """
        Remove a scene from the render targets.

        Args:
            scene: The scene object or its ID.
        """
        if isinstance(scene, str):
            target_id = scene
        else:
            target_id = scene.id

        if target_id not in self.__render_targets:
            Console.log(f"{target_id} is not a render target", LogType.WARNING)
            return

        self.__render_targets.pop(target_id, None)
        Console.log(f"{target_id} is no longer a render target")
        self.update_render_order_list()

    def update_render(self):
        """Render all active scenes in the correct order."""
        Window.window.clear()

        for scene_id in self.__render_order:
            self.__render_targets[scene_id].batch.draw()

        Console.draw()
        Window.window.flip()

    def update_render_order_list(self):
        """
        Sort render targets by z-index and update the render order.
        """
        self.__render_order = [
            scene.id
            for scene in sorted(
                self.__render_targets.values(),
                key=lambda scene: scene.zindex,
            )
        ]

        Console.log(f"Renderer is rendering {len(self.__render_order)} scenes")


Renderer = RendererCls()
__all__ = ["Renderer"]
