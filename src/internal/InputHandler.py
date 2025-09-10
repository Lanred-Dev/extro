from typing import Dict, Tuple, Union, TYPE_CHECKING
import pyray
from enum import Enum

import src.internal.Console as Console
from src.internal.components.Signal import Signal
from src.values.Vector2 import Vector2
import src.internal.Renderer as Renderer

if TYPE_CHECKING:
    from src.shared_types import EmptyFunction


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


class InputSignalConnectionType(Enum):
    PRESS = 0
    RELEASE = 1
    ACTIVE = 2


class _InputSignalType(Enum):
    KEY = 0
    MOUSE = 1


class InputSignal(Signal):
    __slots__ = ("_subscriber_types", "_type")

    _subscriber_types: Dict[str, Tuple[InputSignalConnectionType, Union[Key, Mouse]]]
    _type: _InputSignalType

    def __init__(self, type: _InputSignalType):
        super().__init__()
        self._subscriber_types = {}
        self._type = type

    def connect(
        self,
        callback: "EmptyFunction",
        type: InputSignalConnectionType = InputSignalConnectionType.PRESS,
        input: Union[Key, Mouse] = Key.A,
    ) -> str:
        if self._type == _InputSignalType.KEY and not isinstance(input, Key):
            Console.log(
                "Input must be of type Key for key input signals", Console.LogType.ERROR
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

    def fire_active_inputs(self):
        for connection_id, (type, input) in self._subscriber_types.items():
            match (type):
                case InputSignalConnectionType.PRESS:
                    if pyray.is_key_pressed(input.value):
                        self._subscribers[connection_id](input)
                    elif pyray.is_mouse_button_pressed(input.value):
                        self._subscribers[connection_id](input)
                case InputSignalConnectionType.RELEASE:
                    if pyray.is_key_released(input.value):
                        self._subscribers[connection_id](input)
                    elif pyray.is_mouse_button_released(input.value):
                        self._subscribers[connection_id](input)
                case InputSignalConnectionType.ACTIVE:
                    if input == Mouse.MOVE:
                        if not _mouse_moved:
                            continue
                        Renderer.screen_to_world_coords(_mouse_position)
                        self._subscribers[connection_id](_mouse_position)
                    elif pyray.is_key_down(input.value):
                        self._subscribers[connection_id](input)
                    elif pyray.is_mouse_button_down(input.value):
                        self._subscribers[connection_id](input)


on_key_event: InputSignal = InputSignal(_InputSignalType.KEY)
on_mouse_event: InputSignal = InputSignal(_InputSignalType.MOUSE)


def _update_inputs():
    global _mouse_position, _last_mouse_position, _mouse_moved
    _mouse_position.x = pyray.get_mouse_x()
    _mouse_position.y = pyray.get_mouse_y()

    if _mouse_position != _last_mouse_position:
        _mouse_moved = True
        _last_mouse_position = _mouse_position.copy()
    else:
        _mouse_moved = False

    on_key_event.fire_active_inputs()
    on_mouse_event.fire_active_inputs()


def set_mouse_visibility(is_visible: bool):
    if is_visible:
        pyray.show_cursor()
    else:
        pyray.hide_cursor()


__all__ = [
    "on_key_event",
    "on_mouse_event",
    "_update_inputs",
    "Key",
    "Mouse",
    "InputSignalConnectionType",
    "set_mouse_visibility",
]
