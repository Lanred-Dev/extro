from typing import TYPE_CHECKING
from enum import Enum
import math

import extro.Console as Console
import extro.services.Input as InputService
import extro.internal.InstanceManager as InstanceManager

if TYPE_CHECKING:
    from extro.instances.ui.Button import Button
    from extro.shared.Vector2 import Vector2


class UIInstanceType(Enum):
    GENERIC = 0
    BUTTON = 1


instances: dict[int, UIInstanceType] = {}
type_map: dict[UIInstanceType, list[int]] = {
    UIInstanceType.GENERIC: [],
    UIInstanceType.BUTTON: [],
}


def register(instance_id: int, type: UIInstanceType):
    if instance_id in instances:
        Console.log(
            f"UI instance {instance_id} is already registered", Console.LogType.WARNING
        )
        return

    instances[instance_id] = type
    Console.log(f"Audio source {instance_id} is now registered", Console.LogType.DEBUG)
    recompute_type_maps()


def unregister(instance_id: int):
    if instance_id not in instances:
        Console.log(
            f"UI instance {instance_id} is not registered", Console.LogType.WARNING
        )
        return

    del instances[instance_id]
    Console.log(
        f"UI instance {instance_id} is no longer registered", Console.LogType.DEBUG
    )
    recompute_type_maps()


def recompute_type_maps():
    for key in type_map.keys():
        type_map[key] = []

    for instance_id in instances:
        type_map[instances[instance_id]].append(instance_id)

    Console.log("Recomputed UI instance type maps", Console.LogType.DEBUG)


def handle_click_event(mouse_position: "Vector2"):
    inside_buttons: "list[Button]" = []
    highest_zindex: float = -math.inf

    for instance_id in type_map[UIInstanceType.BUTTON]:
        instance: "Button" = InstanceManager.instances[instance_id]  # type: ignore

        if not instance.is_visible or not instance.is_point_inside(mouse_position):
            continue

        inside_buttons.append(instance)
        highest_zindex = max(highest_zindex, instance._zindex)

    # Prevent buttons under other buttons from being clicked
    for button in inside_buttons:
        if button._zindex < highest_zindex:
            continue

        button.on_click.fire()


InputService.on_mouse_event.connect(
    handle_click_event, InputService.SubscriberType.PRESS, InputService.Mouse.LEFT
)
