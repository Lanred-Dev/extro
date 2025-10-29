from typing import TYPE_CHECKING
import math
import pyray
from enum import Enum, auto, IntFlag
import functools

import extro.Console as Console
import extro.internal.InstanceManager as InstanceManager
import extro.internal.ComponentManager as ComponentManager
from extro.internal.utils.InstanceRegistry import InstanceRegistry
import extro.internal.systems.Input as InputSystem
from extro.shared.Coord import Coord

if TYPE_CHECKING:
    from extro.instances.core.Instance.UI.Clickable import Clickable
    from extro.instances.ui.Text import Text
    from extro.shared.Vector2C import Vector2
    import extro.internal.InstanceManager as InstanceManager
    from extro.instances.core.Instance.UI import UIInstance


class UIInstanceType(Enum):
    CLICKABLE = auto()
    TEXT = auto()


class TextDirtyFlags(IntFlag):
    FONT_SIZE = auto()


instances: InstanceRegistry = InstanceRegistry(
    "UI System", on_list_change=lambda: recompute_type_map()
)
type_map: "dict[UIInstanceType, list[InstanceManager.InstanceID]]" = {
    type: [] for type in UIInstanceType
}
focused_instance: "InstanceManager.InstanceID | None" = None


def recompute_type_map():
    for key in type_map.keys():
        type_map[key] = []

    for instance_id in instances.instances[:]:
        instance: "UIInstance" = InstanceManager.instances[instance_id]  # type: ignore
        type_map[instance._type].append(instance_id)

    Console.log("Recomputed UI instance type maps", Console.LogType.DEBUG)


def handle_click(_, mouse_position: "Vector2"):
    global focused_instance

    clicked_instance: "Clickable | None" = None
    highest_zindex: float = -math.inf

    for instance_id in type_map[UIInstanceType.CLICKABLE][:]:
        transform = ComponentManager.transforms[instance_id]
        drawable = ComponentManager.drawables[instance_id]

        if (
            not drawable.is_visible
            or not transform.is_point_inside(mouse_position)
            or drawable._zindex < highest_zindex
        ):
            continue

        highest_zindex = drawable._zindex
        clicked_instance = InstanceManager.instances[instance_id]  # type: ignore

    if clicked_instance is None:
        return

    clicked_instance.on_click.fire(mouse_position)

    if focused_instance is not None and focused_instance != clicked_instance._id:
        previous_focused: "Clickable" = InstanceManager.instances[focused_instance]  # type: ignore
        previous_focused.on_focus_lost.fire()

    if focused_instance != clicked_instance._id:
        clicked_instance.on_focus.fire()
        focused_instance = clicked_instance._id


@functools.lru_cache(maxsize=32)
def get_size_at_font_size(
    font: "pyray.Font", text: str, font_size: int, character_spacing: int
) -> tuple[float, float]:
    measure: pyray.Vector2 = pyray.measure_text_ex(
        font,
        text,
        font_size,
        character_spacing,
    )
    return (measure.x, measure.y)


def update():
    for instance_id in type_map[UIInstanceType.TEXT][:]:
        instance: "Text" = InstanceManager.instances[instance_id]  # type: ignore

        if not instance.scale_size_to_font or not instance._is_font_size_dirty:
            continue

        size_x, size_y = get_size_at_font_size(
            instance.font(),
            instance.text,
            instance.font_size,
            instance.character_spacing,
        )
        transform = ComponentManager.transforms[instance_id]
        transform.size = Coord(size_x, size_y, Coord.CoordType.ABSOLUTE)
        instance._is_font_size_dirty = False


InputSystem.on_event.connect(
    handle_click, InputSystem.SubscriberType.PRESS, InputSystem.Mouse.LEFT
)
