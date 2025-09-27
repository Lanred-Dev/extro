from typing import TYPE_CHECKING, TypedDict
import pyray

import extro.Console as Console
import extro.services.World as WorldService
import extro.internal.services.Identity as IdentityService
from extro.shared.types import RenderTargetType
import extro.services.Render as RenderService

if TYPE_CHECKING:
    from extro.core.Scene import Scene
    from extro.core.Instance.Drawable import DrawableInstance


class RenderOrder(TypedDict):
    world: list[str]
    independent: list[str]


render_targets: dict[str, "Scene"] = {}
render_order: RenderOrder = {"world": [], "independent": []}


def register(target: "Scene"):
    if getattr(target, "_type", None) not in RenderTargetType:
        # Cant use id for this error message because register is what assigns the id
        Console.log(
            "Scene cannot be registered as a render target because it has no type",
            Console.LogType.ERROR,
        )
        return

    id: str = IdentityService.generate_id(10, "rt_")
    target._id = id
    render_targets[id] = target
    Console.log(f"{id} is now a render target")
    recalculate_render_order()


def unregister(target_id: str):
    if target_id not in render_targets:
        Console.log(f"{target_id} is not a render target", Console.LogType.ERROR)
        return

    render_targets.pop(target_id)
    Console.log(f"{target_id} is no longer a render target")
    recalculate_render_order()


def render():
    RenderService.on_pre_render.fire()

    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)
    pyray.begin_mode_2d(WorldService.camera._camera)

    for target_id in render_order["world"]:
        render_targets[target_id].draw()

    pyray.end_mode_2d()

    for target_id in render_order["independent"]:
        render_targets[target_id].draw()

    Console._draw()
    pyray.end_drawing()

    RenderService.on_post_render.fire()


def recalculate_render_order():
    """Recalculate the render order of all registered render targets."""
    global render_order
    render_order["world"] = []
    render_order["independent"] = []

    for target_id in calculate_render_order(list(render_targets.values())):
        if render_targets[target_id]._type == RenderTargetType.WORLD:
            render_order["world"].append(target_id)
        else:
            render_order["independent"].append(target_id)

    Console.log(
        f"Renderer is rendering {len(render_order['world']) + len(render_order['independent'])} targets"
    )


def calculate_render_order(targets: "list[DrawableInstance | Scene]") -> list:
    """Calculate the render order of the given targets based on their z-index."""
    return [
        target.id
        for target in sorted(
            targets,
            key=lambda target: target._zindex,
        )
    ]
