from typing import TYPE_CHECKING, List, Dict, TypedDict
import pyray

import src.internal.Console as Console
import src.internal.IdentityHandler as IdentityHandler
from src.internal.Window import Window
from src.values.Vector2 import Vector2
from src.shared_types import RenderTargetType

if TYPE_CHECKING:
    from instances.Scene import Scene
    from instances.core.Instance import Instance


class _RenderOrder(TypedDict):
    world: List[str]
    independent: List[str]


_render_targets: Dict[str, "Scene"] = {}
_render_order: _RenderOrder = {"world": [], "independent": []}
world_tile_size: int = 32
camera_position: Vector2 = Vector2(0, 0)


def register_render_target(target: "Scene"):
    if getattr(target, "_type", None) not in RenderTargetType:
        Console.log(
            f"{target.id} cannot be registered as a render target because it has no type",
            Console.LogType.ERROR,
        )
        return

    target.id = IdentityHandler.generate_id(10, "rt_")
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

    for target_id in _render_order["world"]:
        _render_targets[target_id].draw()

    for target_id in _render_order["independent"]:
        _render_targets[target_id].draw()

    Console._draw()
    pyray.end_drawing()


def _recalculate_render_target_order():
    global _render_order

    _render_order["world"] = []
    _render_order["independent"] = []

    new_render_order: List[str] = calculate_render_order(list(_render_targets.values()))
    for target_id in new_render_order:
        if _render_targets[target_id]._type == RenderTargetType.WORLD:
            _render_order["world"].append(target_id)
        else:
            _render_order["independent"].append(target_id)

    Console.log(
        f"Renderer is rendering {len(_render_order['world']) + len(_render_order['independent'])} targets"
    )


def calculate_render_order(targets: "List[Instance | Scene]") -> List[str]:
    return [
        target.id
        for target in sorted(
            targets,
            key=lambda target: target._zindex,
        )
    ]


def normalized_to_screen_coords(vector: Vector2):
    vector.x *= Window._actual_size.x
    vector.y *= Window._actual_size.y


def world_to_screen_coords(vector: Vector2):
    vector.x = (vector.x - camera_position.x) * world_tile_size
    vector.y = (vector.y - camera_position.y) * world_tile_size


def screen_to_world_coords(vector: Vector2):
    vector.x = (vector.x / world_tile_size) + camera_position.x
    vector.y = (vector.y / world_tile_size) + camera_position.y


def set_world_tile_size(size: int):
    global world_tile_size

    if size <= 0:
        Console.log("World tile size must be greater than 0", Console.LogType.ERROR)
        return

    world_tile_size = size
    Console.log(f"World tile size set to {world_tile_size}")


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
    "world_tile_size",
]
