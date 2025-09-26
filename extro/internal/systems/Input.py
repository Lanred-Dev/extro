from typing import TYPE_CHECKING
import pyray
from enum import IntEnum

import extro.Console as Console
from extro.utils.Signal import Signal
from extro.shared.Vector2 import Vector2

if TYPE_CHECKING:
    from extro.shared.types import EmptyFunction


class Key(IntEnum):
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


class Mouse(IntEnum):
    LEFT = pyray.MouseButton.MOUSE_BUTTON_LEFT
    RIGHT = pyray.MouseButton.MOUSE_BUTTON_RIGHT
    MIDDLE = pyray.MouseButton.MOUSE_BUTTON_MIDDLE
    MOVE = -1


ALL_KEYS: list[Key] = [key for key in Key]
ALL_MOUSE_BUTTONS: list[Mouse] = [Mouse.LEFT, Mouse.RIGHT, Mouse.MIDDLE]

mouse_position: Vector2 = Vector2(0, 0)
active_inputs: dict[int, bool] = {key: False for key in ALL_KEYS + ALL_MOUSE_BUTTONS}
old_active_inputs: dict[int, bool] = active_inputs.copy()


class SubscriberType(IntEnum):
    PRESS = 0
    RELEASE = 1
    ACTIVE = 2


class InternalSignalType(IntEnum):
    KEY = 0
    MOUSE = 1


class InputSignal(Signal):
    __slots__ = ("_subscriber_types", "_type")

    _subscriber_types: dict[str, tuple[SubscriberType, Key | Mouse | None]]
    _type: InternalSignalType

    def __init__(self, type: InternalSignalType):
        super().__init__()
        self._subscriber_types = {}
        self._type = type

    def connect(
        self,
        callback: "EmptyFunction",
        type: SubscriberType = SubscriberType.PRESS,
        input: Key | Mouse | None = None,
    ) -> str:
        if input is not None:
            if self._type == InternalSignalType.KEY and not isinstance(input, Key):
                Console.log(
                    "Input must be of type Key for key input signals",
                    Console.LogType.ERROR,
                )
                return ""
            if self._type == InternalSignalType.MOUSE and not isinstance(input, Mouse):
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
        self, type: SubscriberType, input: Key | Mouse, *args
    ):
        for connection_id, (
            subscriber_type,
            subscriber_input,
        ) in self._subscriber_types.items():
            if subscriber_type is not type or (
                subscriber_input is not None and subscriber_input != input
            ):
                continue

            self._subscribers[connection_id](input, *args)


on_key_event: InputSignal = InputSignal(InternalSignalType.KEY)
on_mouse_event: InputSignal = InputSignal(InternalSignalType.MOUSE)


def update_inputs():
    global mouse_position, active_inputs
    new_mouse_x = pyray.get_mouse_x()
    new_mouse_y = pyray.get_mouse_y()

    if new_mouse_x != mouse_position.x or new_mouse_y != mouse_position.y:
        mouse_position.x = new_mouse_x
        mouse_position.y = new_mouse_y
        on_mouse_event.fire_subscribers_with_filter(SubscriberType.ACTIVE, Mouse.MOVE)

    for key in ALL_KEYS:
        active_inputs[key] = pyray.is_key_down(key)

        if active_inputs[key]:
            on_key_event.fire_subscribers_with_filter(SubscriberType.ACTIVE, key)

            if not old_active_inputs[key]:
                on_key_event.fire_subscribers_with_filter(SubscriberType.PRESS, key)
        elif not active_inputs[key] and old_active_inputs[key]:
            on_key_event.fire_subscribers_with_filter(SubscriberType.RELEASE, key)

        old_active_inputs[key] = active_inputs[key]

    for mouse in ALL_MOUSE_BUTTONS:
        active_inputs[mouse] = pyray.is_mouse_button_down(mouse)

        if active_inputs[mouse] and not old_active_inputs[mouse]:
            on_mouse_event.fire_subscribers_with_filter(
                SubscriberType.PRESS, mouse, mouse_position
            )
        elif not active_inputs[mouse] and old_active_inputs[mouse]:
            on_mouse_event.fire_subscribers_with_filter(
                SubscriberType.RELEASE, mouse, mouse_position
            )

        old_active_inputs[mouse] = active_inputs[mouse]
