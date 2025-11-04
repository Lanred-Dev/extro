from typing import TYPE_CHECKING
import pyray
from enum import IntEnum

from extro.utils.Signal import Signal
from extro.shared.Vector2C import Vector2

if TYPE_CHECKING:
    from extro.shared.types import EmptyFunction
    import extro.internal.InstanceManager as InstanceManager


class Keyboard(IntEnum):
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

    COMMA = pyray.KeyboardKey.KEY_COMMA
    PERIOD = pyray.KeyboardKey.KEY_PERIOD
    SEMICOLON = pyray.KeyboardKey.KEY_SEMICOLON
    APOSTROPHE = pyray.KeyboardKey.KEY_APOSTROPHE
    SLASH = pyray.KeyboardKey.KEY_SLASH
    BACKSLASH = pyray.KeyboardKey.KEY_BACKSLASH
    LEFT_BRACKET = pyray.KeyboardKey.KEY_LEFT_BRACKET
    RIGHT_BRACKET = pyray.KeyboardKey.KEY_RIGHT_BRACKET
    MINUS = pyray.KeyboardKey.KEY_MINUS
    EQUALS = pyray.KeyboardKey.KEY_EQUAL


class KeyboardModifiers(IntEnum):
    SHIFT = pyray.KeyboardKey.KEY_LEFT_SHIFT
    CTRL = pyray.KeyboardKey.KEY_LEFT_CONTROL
    ALT = pyray.KeyboardKey.KEY_LEFT_ALT


class Mouse(IntEnum):
    LEFT = pyray.MouseButton.MOUSE_BUTTON_LEFT
    RIGHT = pyray.MouseButton.MOUSE_BUTTON_RIGHT
    MIDDLE = pyray.MouseButton.MOUSE_BUTTON_MIDDLE
    MOVE = -1


mouse_position: Vector2 = Vector2(0, 0)
active_inputs: dict[int, bool] = {
    key: False
    for key in [key for key in Keyboard] + [Mouse.LEFT, Mouse.RIGHT, Mouse.MIDDLE]
}
old_active_inputs: dict[int, bool] = active_inputs.copy()
input_usage_map: dict[int, int] = {}
input_captured_by: "InstanceManager.InstanceID | None" = None
all_inputs: tuple[Keyboard | Mouse] = tuple(key for key in Keyboard) + (Mouse.LEFT, Mouse.RIGHT, Mouse.MIDDLE)  # type: ignore


def add_input_usage(input: Keyboard | Mouse):
    if input not in input_usage_map:
        input_usage_map[input] = 0

    input_usage_map[input] += 1


def remove_input_usage(input: Keyboard | Mouse):
    if input not in input_usage_map:
        return

    input_usage_map[input] -= 1

    if input_usage_map[input] <= 0:
        del input_usage_map[input]


class SubscriberType(IntEnum):
    PRESS = 0
    RELEASE = 1
    ACTIVE = 2


class InputSignal(Signal):
    __slots__ = Signal.__slots__ + ("_subscriber_input_map", "_subscriber_type_map")

    _subscriber_input_map: dict[SubscriberType, dict[str, tuple[Keyboard | Mouse, ...]]]
    _subscriber_type_map: dict[str, SubscriberType]

    def __init__(self):
        super().__init__()

        self._subscriber_input_map = {type: {} for type in SubscriberType}
        self._subscriber_type_map = {}

    def connect(
        self,
        callback: "EmptyFunction",
        type: SubscriberType = SubscriberType.PRESS,
        inputs: Keyboard | Mouse | tuple[Keyboard | Mouse, ...] | None = None,
    ) -> str:
        connection_id = super().connect(callback)

        actual_inputs: tuple[Keyboard | Mouse, ...] = (
            inputs
            if isinstance(inputs, tuple)
            else (inputs,) if inputs is not None else all_inputs
        )
        self._subscriber_type_map[connection_id] = type
        self._subscriber_input_map[type][connection_id] = actual_inputs

        for input in actual_inputs:
            add_input_usage(input)

        return connection_id

    def disconnect(self, connection_id: str):
        super().disconnect(connection_id)

        for input in self._subscriber_input_map[
            self._subscriber_type_map[connection_id]
        ][connection_id]:
            remove_input_usage(input)

        del self._subscriber_input_map[self._subscriber_type_map[connection_id]][
            connection_id
        ]
        del self._subscriber_type_map[connection_id]

    def _fire_subscribers_with_filter(self, type: SubscriberType, input: int, *args):
        for connection_id, inputs in self._subscriber_input_map[type].copy().items():
            if input not in inputs or connection_id not in self._subscribers:
                continue

            self._subscribers[connection_id](input, *args)


on_event: InputSignal = InputSignal()


def update():
    global mouse_position, active_inputs
    new_mouse_x = pyray.get_mouse_x()
    new_mouse_y = pyray.get_mouse_y()

    if new_mouse_x != mouse_position.x or new_mouse_y != mouse_position.y:
        mouse_position.x = new_mouse_x
        mouse_position.y = new_mouse_y
        on_event._fire_subscribers_with_filter(
            SubscriberType.ACTIVE, Mouse.MOVE, mouse_position
        )

    for input in input_usage_map.copy():
        if input == Mouse.MOVE:
            continue

        active_inputs[input] = (
            pyray.is_key_down(input)
            if input in Keyboard
            else pyray.is_mouse_button_down(input)
        )
        args = (mouse_position,) if input in Mouse else ()

        if active_inputs[input]:
            on_event._fire_subscribers_with_filter(SubscriberType.ACTIVE, input, *args)

            if not old_active_inputs[input]:
                on_event._fire_subscribers_with_filter(
                    SubscriberType.PRESS, input, *args
                )
        elif not active_inputs[input] and old_active_inputs[input]:
            on_event._fire_subscribers_with_filter(SubscriberType.RELEASE, input, *args)

        old_active_inputs[input] = active_inputs[input]


def request_keyboard_capture(instance_id: "InstanceManager.InstanceID") -> bool:
    global input_captured_by

    if input_captured_by is not None:
        return False

    input_captured_by = instance_id
    return True


def release_keyboard_capture():
    global input_captured_by
    input_captured_by = None
