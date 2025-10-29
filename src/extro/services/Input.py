"""Provides input-related constants, types, events, and access to the input action system."""

import pyray
from typing import TYPE_CHECKING

import extro.Console as Console
import extro.internal.systems.Input as InputSystem

if TYPE_CHECKING:
    from extro.shared.Vector2C import Vector2
    import extro.internal.InstanceManager as InstanceManager

Key = InputSystem.Key
Mouse = InputSystem.Mouse
SubscriberType = InputSystem.SubscriberType
on_event: InputSystem.InputSignal = InputSystem.on_event
mouse_position: "Vector2" = InputSystem.mouse_position
input_captured_by: "InstanceManager.InstanceID | None" = InputSystem.input_captured_by
request_keyboard_capture = InputSystem.request_keyboard_capture
release_keyboard_capture = InputSystem.release_keyboard_capture
_actions: dict[str, int] = {}


def register_action(id: str, input: int):
    if input in _actions.values():
        Console.log(f"Input {input} is already being used", Console.LogType.WARNING)
        return
    elif id in _actions:
        Console.log(f"Input action {id} is already registered", Console.LogType.WARNING)
        return

    _actions[id] = input
    Console.log(f"Registered input action {id} with {input}", Console.LogType.DEBUG)


def unregister_action(id: str):
    if id not in _actions:
        Console.log(f"Input action {id} is not registered", Console.LogType.WARNING)
        return

    del _actions[id]
    Console.log(f"Unregistered input action {id}", Console.LogType.DEBUG)


def set_action(id: str, input: int):
    # This is almost the same function as `register_action` but its intended to force the developer to have good code semantics
    if id not in _actions:
        Console.log(f"Input action {id} is not registered", Console.LogType.WARNING)
        return
    elif input in _actions.values():
        Console.log(f"Input {input} is already being used", Console.LogType.WARNING)
        return

    _actions[id] = input
    Console.log(f"Set input action {id} to {input}", Console.LogType.DEBUG)


def get_action(id: str) -> int | None:
    """Returns the value of the input action if it exists."""
    return _actions.get(id, None)


def set_mouse_visibility(is_visible: bool):
    if is_visible:
        pyray.show_cursor()
    else:
        pyray.hide_cursor()

    Console.log(f"Mouse visibility set to {is_visible}", Console.LogType.DEBUG)


def is_input_active(input: InputSystem.Key | InputSystem.Mouse) -> bool:
    return InputSystem.active_inputs[input]


__all__ = [
    "Key",
    "Mouse",
    "SubscriberType",
    "on_event",
    "set_mouse_visibility",
    "is_input_active",
    "register_action",
    "unregister_action",
    "get_action",
    "set_action",
    "mouse_position",
    "input_captured_by",
    "request_keyboard_capture",
    "release_keyboard_capture",
]
