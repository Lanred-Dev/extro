from typing import TYPE_CHECKING
import pyray
from enum import IntFlag, auto

from extro.internal.utils.InstanceRegistry import InstanceRegistry
import extro.services.Timing as TimingService
import extro.services.World as WorldService
import extro.Console as Console
import extro.services.Render as RenderService
import extro.internal.InstanceManager as InstanceManager

if TYPE_CHECKING:
    import extro.internal.InstanceManager as InstanceManager
    from extro.instances.core.RenderTarget import RenderTarget


class DrawableDirtyFlags(IntFlag):
    ZINDEX = auto()
    IS_VISIBLE = auto()


class RenderTargetDirtyFlags(IntFlag):
    ZINDEX = auto()
    RENDER_ORDER = auto()


render_targets: InstanceRegistry = InstanceRegistry(
    "Render System",
    on_list_change=lambda: recalculate_render_order(),
)
render_order: "list[list[RenderTarget]]" = [[], []]  # 0 = world, 1 = independent
is_dirty: bool = False


def draw_render_target(target: "RenderTarget"):
    if not target.is_visible:
        return

    target.draw()


def render():
    should_recalculate_render_order: bool = False

    for target_id in render_targets.instances[:]:
        target: "RenderTarget" = InstanceManager.instances[target_id]  # type: ignore

        if target.bitmask._flags == 0:
            continue

        if target.bitmask.has_flag(RenderTargetDirtyFlags.ZINDEX):
            should_recalculate_render_order = True

        if target.bitmask.has_flag(RenderTargetDirtyFlags.RENDER_ORDER):
            target._render_order = calculate_render_order(target._instances.instances)

        target.bitmask.clear_flags()

    if should_recalculate_render_order:
        recalculate_render_order()

    TimingService.on_pre_render.fire()

    pyray.begin_drawing()
    pyray.clear_background(pyray.BLACK)
    pyray.begin_mode_2d(WorldService.camera._camera)

    for instance in render_order[0]:
        draw_render_target(instance)

    pyray.end_mode_2d()

    for instance in render_order[1]:
        draw_render_target(instance)

    Console._draw()
    pyray.end_drawing()

    TimingService.on_post_render.fire()


def recalculate_render_order():
    global render_order
    render_order = [[], []]

    sorted_targets: "list[RenderTarget]" = sorted(
        (
            InstanceManager.instances[target_id]
            for target_id in render_targets.instances[:]
        ),
        key=lambda target: target.zindex,  # type: ignore
    )

    for target in sorted_targets:
        (
            render_order[0]
            if target._type == RenderService.RenderTargetType.WORLD
            else render_order[1]
        ).append(target)

    Console.log(
        f"Render System is rendering {sum(len(targets) for targets in render_order)} targets"
    )


def calculate_render_order(
    targets: "list[InstanceManager.InstanceIDType]",
) -> "list[InstanceManager.InstanceIDType]":
    instances = [InstanceManager.instances[target] for target in targets]
    return [
        instance.id
        for instance in sorted(
            instances,
            key=lambda instance: instance.get_component_unsafe("drawable")._zindex,
        )
    ]
