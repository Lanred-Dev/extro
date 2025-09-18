from typing import TYPE_CHECKING, TypedDict
import pyray

import src.internal.Console as Console
from src.internal.services import WorldService
import src.internal.services.IdentityService as IdentityService
from src.internal.shared_types import RenderTargetType

if TYPE_CHECKING:
    from src.instances.core.Scene import Scene
    from instances.core.DrawableInstance import DrawableInstance


class _RenderOrder(TypedDict):
    world: list[str]
    independent: list[str]


_render_targets: dict[str, "Scene"] = {}
_render_order: _RenderOrder = {"world": [], "independent": []}


def register_render_target(target: "Scene"):
    if getattr(target, "_type", None) not in RenderTargetType:
        Console.log(
            f"{target.id} cannot be registered as a render target because it has no type",
            Console.LogType.ERROR,
        )
        return

    target.id = IdentityService.generate_id(10, "rt_")
    _render_targets[target.id] = target
    Console.log(f"{target.id} is now a render target")
    _recalculate_render_target_order()


def unregister_render_target(target_id: str):
    if target_id not in _render_targets:
        Console.log(f"{target_id} is not a render target", Console.LogType.ERROR)
        return

    _render_targets.pop(target_id)
    Console.log(f"{target_id} is no longer a render target")
    _recalculate_render_target_order()


def _render():
    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)

    if WorldService._camera:
        pyray.begin_mode_2d(WorldService._camera)

    for target_id in _render_order["world"]:
        _render_targets[target_id].draw()

    if WorldService._camera:
        pyray.end_mode_2d()

    for target_id in _render_order["independent"]:
        _render_targets[target_id].draw()

    Console._draw()
    pyray.end_drawing()


def _recalculate_render_target_order():
    global _render_order

    _render_order["world"] = []
    _render_order["independent"] = []

    new_render_order: list[str] = calculate_render_order(list(_render_targets.values()))
    for target_id in new_render_order:
        if _render_targets[target_id]._type == RenderTargetType.WORLD:
            _render_order["world"].append(target_id)
        else:
            _render_order["independent"].append(target_id)

    Console.log(
        f"Renderer is rendering {len(_render_order['world']) + len(_render_order['independent'])} targets"
    )


def calculate_render_order(targets: "list[DrawableInstance | Scene]") -> list[str]:
    return [
        target.id
        for target in sorted(
            targets,
            key=lambda target: target._zindex,
        )
    ]


def set_fps(fps: int):
    if fps <= 0:
        Console.log("FPS must be greater than 0", Console.LogType.ERROR)
        return

    pyray.set_target_fps(fps)
    Console.log(f"Target FPS set to {fps}")


# `RenderTargetType` is re-exported here for unified access to the developer
__all__ = [
    "register_render_target",
    "unregister_render_target",
    "_render",
    "_recalculate_render_target_order",
    "calculate_render_order",
    "RenderTargetType",
]
