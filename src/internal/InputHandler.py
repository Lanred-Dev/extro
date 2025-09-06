import pyglet
from pyglet.window import mouse
from typing import List

from src.internal.Window import Window
from src.internal.components.Signal import Signal


class InputHandlerCls:
    on_key_press: Signal
    on_key_release: Signal
    on_mouse_move: Signal
    on_mouse_click: Signal
    __active: List[int]

    def __init__(self):
        self.on_key_press = Signal()
        self.on_key_release = Signal()
        self.on_mouse_move = Signal()
        self.on_mouse_click = Signal()
        self.__active = []
        Window.window.push_handlers(
            on_key_press=self.__handle_key_press,
            on_key_release=self.__handle_key_release,
            on_mouse_motion=self.__handle_mouse_move,
            on_mouse_press=self.__handle_mouse_click,
        )

    def is_key_active(self, key: int):
        return key in self.__active

    def __handle_key_press(self, key: int, modifiers: List[int]):
        self.__active.append(key)
        self.on_key_press.fire(key, modifiers)

    def __handle_key_release(self, key: int, modifiers: List[int]):
        self.__active.remove(key)
        self.on_key_release.fire(key, modifiers)

    def __handle_mouse_click(self, x: int, y: int, button: int, modifiers: List[int]):
        self.on_mouse_click.fire(button, x, y, modifiers)

    def __handle_mouse_move(self, x: int, y: int, _dx: int, _dy: int):
        self.on_mouse_move.fire(x, y)


InputHandler = InputHandlerCls()
KeyMapping = pyglet.window.key
MouseButtonMapping = mouse
__all__ = ["InputHandler", "KeyMapping", "MouseButtonMapping"]
