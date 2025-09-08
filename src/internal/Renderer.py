from typing import TYPE_CHECKING, List, Dict

from src.internal.Window import Window
from src.internal.Console import Console, LogType
from src.internal.IdentityHandler import generate_id

if TYPE_CHECKING:
    from instances.Scene import Scene


class RendererCls:
    """
    Central renderer manager for handling scenes and rendering order.

    Keeps track of active render targets (scenes) and ensures they
    are rendered in the correct order based on z-index.
    """

    _render_targets: Dict[str, "Scene"]
    _render_order: List[str]

    def __init__(self):
        self._render_targets = {}
        self._render_order = []

    def register_render_target(self, target: "Scene"):
        """
        Add a scene as a render target.

        Args:
            scene: The scene to register for rendering.
        """
        target_id: str = generate_id(10, "rt_")
        target.id = target_id
        self._render_targets[target_id] = target
        Console.log(f"{target_id} is now a render target")
        self.update_render_order()

    def unregister_render_target(self, target: "Scene | str"):
        """
        Remove a scene from the render targets.

        Args:
            scene: The scene object or its ID.
        """
        if isinstance(target, str):
            target_id = target
        else:
            target_id = target.id

        if target_id not in self._render_targets:
            Console.log(f"{target_id} is not a render target", LogType.WARNING)
            return

        self._render_targets.pop(target_id, None)
        Console.log(f"{target_id} is no longer a render target")
        self.update_render_order()

    def render(self):
        """Render all active scenes in the correct order."""
        Window.clear()

        for scene_id in self._render_order:
            self._render_targets[scene_id]._batch.draw()

        Console.draw()
        Window.flip()

    def update_render_order(self):
        """
        Sort render targets by z-index and update the render order.
        """
        self._render_order = [
            scene.id
            for scene in sorted(
                self._render_targets.values(),
                key=lambda target: target._zindex,
            )
        ]

        Console.log(f"Renderer is rendering {len(self._render_order)} scenes")


Renderer = RendererCls()
__all__ = ["Renderer"]
