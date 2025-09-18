from typing import TYPE_CHECKING
import pyray
from enum import Enum

import src.internal.Console as Console
from src.internal.helpers.Signal import Signal
from src.values.Vector2 import Vector2
import src.internal.services.ScreenService as ScreenService

if TYPE_CHECKING:
    from src.internal.shared_types import EmptyFunction


class Key(Enum):
    # Letter keys
    A = pyray.KeyboardKey.KEY_A
    B = pyray.KeyboardKey.KEY_B
    C = pyray.KeyboardKey.KEY_C
    D = pyray.KeyboardKey.KEY_D
    E = pyray.KeyboardKey.KEY_E
    F = pyray.KeyboardKey.KEY_F
    G = pyray.KeyboardKey.KEY_G
    H = pyray.KeyboardKey.KEY_H
    I = pyray.KeyboardKey.KEY_I
    J = pyray.KeyboardKey.KEY_J
    K = pyray.KeyboardKey.KEY_K
    L = pyray.KeyboardKey.KEY_L
    M = pyray.KeyboardKey.KEY_M
    N = pyray.KeyboardKey.KEY_N
    O = pyray.KeyboardKey.KEY_O
    P = pyray.KeyboardKey.KEY_P
    Q = pyray.KeyboardKey.KEY_Q
    R = pyray.KeyboardKey.KEY_R
    S = pyray.KeyboardKey.KEY_S
    T = pyray.KeyboardKey.KEY_T
    U = pyray.KeyboardKey.KEY_U
    V = pyray.KeyboardKey.KEY_V
    W = pyray.KeyboardKey.KEY_W
    X = pyray.KeyboardKey.KEY_X
    Y = pyray.KeyboardKey.KEY_Y
    Z = pyray.KeyboardKey.KEY_Z

    # Number keys
    ZERO = pyray.KeyboardKey.KEY_ZERO
    ONE = pyray.KeyboardKey.KEY_ONE
    TWO = pyray.KeyboardKey.KEY_TWO
    THREE = pyray.KeyboardKey.KEY_THREE
    FOUR = pyray.KeyboardKey.KEY_FOUR
    FIVE = pyray.KeyboardKey.KEY_FIVE
    SIX = pyray.KeyboardKey.KEY_SIX
    SEVEN = pyray.KeyboardKey.KEY_SEVEN
    EIGHT = pyray.KeyboardKey.KEY_EIGHT
    NINE = pyray.KeyboardKey.KEY_NINE

    # Function keys
    F1 = pyray.KeyboardKey.KEY_F1
    F2 = pyray.KeyboardKey.KEY_F2
    F3 = pyray.KeyboardKey.KEY_F3
    F4 = pyray.KeyboardKey.KEY_F4
    F5 = pyray.KeyboardKey.KEY_F5
    F6 = pyray.KeyboardKey.KEY_F6
    F7 = pyray.KeyboardKey.KEY_F7
    F8 = pyray.KeyboardKey.KEY_F8
    F9 = pyray.KeyboardKey.KEY_F9
    F10 = pyray.KeyboardKey.KEY_F10
    F11 = pyray.KeyboardKey.KEY_F11
    F12 = pyray.KeyboardKey.KEY_F12

    UP = pyray.KeyboardKey.KEY_UP
    DOWN = pyray.KeyboardKey.KEY_DOWN
    LEFT = pyray.KeyboardKey.KEY_LEFT
    RIGHT = pyray.KeyboardKey.KEY_RIGHT

    SPACE = pyray.KeyboardKey.KEY_SPACE
    ENTER = pyray.KeyboardKey.KEY_ENTER
    ESCAPE = pyray.KeyboardKey.KEY_ESCAPE
    TAB = pyray.KeyboardKey.KEY_TAB
    BACKSPACE = pyray.KeyboardKey.KEY_BACKSPACE
    SHIFT = pyray.KeyboardKey.KEY_LEFT_SHIFT
    CTRL = pyray.KeyboardKey.KEY_LEFT_CONTROL
    ALT = pyray.KeyboardKey.KEY_LEFT_ALT


class Mouse(Enum):
    LEFT = pyray.MouseButton.MOUSE_BUTTON_LEFT
    RIGHT = pyray.MouseButton.MOUSE_BUTTON_RIGHT
    MIDDLE = pyray.MouseButton.MOUSE_BUTTON_MIDDLE
    MOVE = -1


_mouse_position: Vector2 = Vector2(0, 0)
_last_mouse_position: Vector2 = Vector2(0, 0)
_mouse_moved: bool = False
_active_inputs: set[Key | Mouse] = set()


class InputSignalConnectionType(Enum):
    PRESS = 0
    RELEASE = 1
    ACTIVE = 2


class _InputSignalType(Enum):
    KEY = 0
    MOUSE = 1


class InputSignal(Signal):
    __slots__ = ("_subscriber_types", "_type")

    _subscriber_types: dict[str, tuple[InputSignalConnectionType, Key | Mouse | None]]
    _type: _InputSignalType

    def __init__(self, type: _InputSignalType):
        super().__init__()
        self._subscriber_types = {}
        self._type = type

    def connect(
        self,
        callback: "EmptyFunction",
        type: InputSignalConnectionType = InputSignalConnectionType.PRESS,
        input: Key | Mouse | None = None,
    ) -> str:
        if input is not None:
            if self._type == _InputSignalType.KEY and not isinstance(input, Key):
                Console.log(
                    "Input must be of type Key for key input signals",
                    Console.LogType.ERROR,
                )
                return ""
            if self._type == _InputSignalType.MOUSE and not isinstance(input, Mouse):
                Console.log(
                    "Input must be of type Mouse for mouse input signals",
                    Console.LogType.ERROR,
                )
                return ""

        connection_id = super().connect(callback)
        self._subscriber_types[connection_id] = (type, input)
        return connection_id

    def disconnect(self, connection_id: str):
        super().disconnect(connection_id)
        del self._subscriber_types[connection_id]

    def fire_subscribers_with_filter(
        self, type: InputSignalConnectionType, input: Key | Mouse
    ):
        for connection_id, (
            subscriber_type,
            subscriber_input,
        ) in self._subscriber_types.items():
            if subscriber_type is not type or (
                subscriber_input is not None and subscriber_input != input
            ):
                continue

            if isinstance(input, Mouse):
                self._subscribers[connection_id](_mouse_position)
            elif subscriber_input is None:
                self._subscribers[connection_id](input)
            else:
                self._subscribers[connection_id]()


on_key_event: InputSignal = InputSignal(_InputSignalType.KEY)
on_mouse_event: InputSignal = InputSignal(_InputSignalType.MOUSE)


def _update():
    global _mouse_position, _last_mouse_position, _mouse_moved, _active_inputs
    _mouse_position.x = pyray.get_mouse_x()
    _mouse_position.y = pyray.get_mouse_y()
    _mouse_moved = _mouse_position != _last_mouse_position

    if _mouse_moved:
        _last_mouse_position = _mouse_position.copy()
        on_mouse_event.fire_subscribers_with_filter(
            InputSignalConnectionType.ACTIVE, Mouse.MOVE
        )

    new_inputs: set[Key | Mouse] = set()

    for key in Key:
        if not pyray.is_key_down(key.value):
            continue

        new_inputs.add(key)

    for mouse in Mouse:
        if mouse == Mouse.MOVE or not pyray.is_mouse_button_down(mouse.value):
            continue

        new_inputs.add(mouse)

    old_inputs = _active_inputs.copy()
    _active_inputs = new_inputs

    # Determine which inputs where released
    for input in old_inputs:
        if input in new_inputs:
            continue

        (
            on_key_event if isinstance(input, Key) else on_mouse_event
        ).fire_subscribers_with_filter(InputSignalConnectionType.RELEASE, input)

    # Determine which inputs where pressed
    for input in new_inputs:
        is_key: bool = isinstance(input, Key)

        # Also fire ACTIVE for pressed inputs
        (on_key_event if is_key else on_mouse_event).fire_subscribers_with_filter(
            InputSignalConnectionType.ACTIVE, input
        )

        if input in old_inputs:
            continue

        (on_key_event if is_key else on_mouse_event).fire_subscribers_with_filter(
            InputSignalConnectionType.PRESS, input
        )


def set_mouse_visibility(is_visible: bool):
    if is_visible:
        pyray.show_cursor()
    else:
        pyray.hide_cursor()


def is_input_active(input: Key | Mouse) -> bool:
    return input in _active_inputs


__all__ = [
    "on_key_event",
    "on_mouse_event",
    "_update",
    "Key",
    "Mouse",
    "InputSignalConnectionType",
    "set_mouse_visibility",
    "is_input_active",
]
