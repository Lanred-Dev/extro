"""Provides input-related constants, types, events, and access to the input action system."""

from unittest import case
import pyray
from typing import TYPE_CHECKING

import extro.Console as Console
import extro.internal.systems.Input as InputSystem

if TYPE_CHECKING:
    from extro.shared.Vector2 import Vector2
    import extro.internal.InstanceManager as InstanceManager

Keyboard = InputSystem.Keyboard
KeyboardModifiers = InputSystem.KeyboardModifiers
Mouse = InputSystem.Mouse
SubscriberType = InputSystem.SubscriberType
on_event: InputSystem.InputSignal = InputSystem.on_event
mouse_position: "Vector2" = InputSystem.mouse_position
input_captured_by: "InstanceManager.InstanceID | None" = InputSystem.input_captured_by
request_keyboard_capture = InputSystem.request_keyboard_capture
release_keyboard_capture = InputSystem.release_keyboard_capture
_actions: dict[str, Keyboard | Mouse] = {}
_uppercase_map: dict[Keyboard, str] = {
    Keyboard.ONE: "!",
    Keyboard.TWO: "@",
    Keyboard.THREE: "#",
    Keyboard.FOUR: "$",
    Keyboard.FIVE: "%",
    Keyboard.SIX: "^",
    Keyboard.SEVEN: "&",
    Keyboard.EIGHT: "*",
    Keyboard.NINE: "(",
    Keyboard.ZERO: ")",
    Keyboard.MINUS: "_",
    Keyboard.EQUALS: "+",
    Keyboard.LEFT_BRACKET: "{",
    Keyboard.RIGHT_BRACKET: "}",
    Keyboard.SEMICOLON: ":",
    Keyboard.APOSTROPHE: '"',
    Keyboard.SLASH: "?",
    Keyboard.BACKSLASH: "|",
}
_number_keys: list[Keyboard] = [
    Keyboard.ONE,
    Keyboard.TWO,
    Keyboard.THREE,
    Keyboard.FOUR,
    Keyboard.FIVE,
    Keyboard.SIX,
    Keyboard.SEVEN,
    Keyboard.EIGHT,
    Keyboard.NINE,
    Keyboard.ZERO,
]


def register_action(id: str, input: Keyboard | Mouse):
    if input in _actions.values():
        Console.log(f"Input {input} is already being used", Console.LogType.WARNING)
        return
    elif id in _actions:
        Console.log(f"Input action {id} is already registered", Console.LogType.WARNING)
        return

    _actions[id] = input
    InputSystem.add_input_usage(input)
    Console.log(f"Registered input action {id} as {input.name}", Console.LogType.DEBUG)


def unregister_action(id: str):
    if id not in _actions:
        Console.log(f"Input action {id} is not registered", Console.LogType.WARNING)
        return

    InputSystem.remove_input_usage(_actions[id])
    del _actions[id]
    Console.log(f"Unregistered input action {id}", Console.LogType.DEBUG)


def set_action(id: str, input: Keyboard | Mouse):
    # This is almost the same function as `register_action` but its intended to force the developer to have good code semantics
    if id not in _actions:
        Console.log(f"Input action {id} is not registered", Console.LogType.WARNING)
        return
    elif input in _actions.values():
        Console.log(f"Input {input} is already being used", Console.LogType.WARNING)
        return

    _actions[id] = input
    Console.log(f"Set input action {id} to {input.name}", Console.LogType.DEBUG)


def get_action(id: str) -> Keyboard | Mouse | None:
    """Returns the value of the input action if it exists."""
    return _actions.get(id, None)


def is_action_active(id: str) -> bool:
    """Returns whether the input action is currently active."""
    input = get_action(id)

    if input is None:
        Console.log(f"Input action {id} is not registered", Console.LogType.WARNING)
        return False

    return InputSystem.active_inputs.get(input, False)


def set_mouse_visibility(is_visible: bool):
    if is_visible:
        pyray.show_cursor()
    else:
        pyray.hide_cursor()

    Console.log(f"Mouse visibility set to {is_visible}", Console.LogType.DEBUG)


def is_input_active(input: Keyboard | Mouse) -> bool:
    return InputSystem.active_inputs[input]


def keycode_to_character(
    input: Keyboard, modifiers: tuple[KeyboardModifiers] | None = None
) -> str | None:
    """Converts a Keyboard input to its corresponding character, if applicable."""
    match input:
        case Keyboard.SPACE:
            return " "
        case (
            Keyboard.ENTER
            | Keyboard.ESCAPE
            | Keyboard.BACKSPACE
            | Keyboard.SHIFT
            | Keyboard.CTRL
            | Keyboard.ALT
            | Keyboard.TAB
            | Keyboard.F1
            | Keyboard.F2
            | Keyboard.F3
            | Keyboard.F4
            | Keyboard.F5
            | Keyboard.F6
            | Keyboard.F7
            | Keyboard.F8
            | Keyboard.F9
            | Keyboard.F10
            | Keyboard.F11
            | Keyboard.F12
        ):
            return None
        case _:
            is_shift_pressed: bool = (
                modifiers is not None and KeyboardModifiers.SHIFT in modifiers
            )

            if is_shift_pressed and input in _uppercase_map:
                return _uppercase_map[input]
            elif input in _number_keys:
                return chr(input.value)

            character: str = chr(input.value)

            if is_shift_pressed:
                character = character.upper()
            else:
                character = character.lower()

            return character


__all__ = [
    "Keyboard",
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
    "keycode_to_character",
]
