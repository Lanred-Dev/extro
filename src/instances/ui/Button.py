import pyray

import src.internal.services.InputService as InputService
from src.instances.core.DrawableInstance import DrawableInstance
from src.values.Vector2 import Vector2
from src.internal.helpers.Signal import Signal


class Button(DrawableInstance):
    __slots__ = ("_rect", "signal")

    _rect: pyray.Rectangle
    on_click: Signal

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._rect = pyray.Rectangle(
            self._actual_position.x,
            self._actual_position.y,
            self._actual_size.x,
            self._actual_size.y,
        )
        self.on_click = Signal()

        InputService.on_mouse_event.connect(
            self._handle_mouse_click,
            type=InputService.InputSignalConnectionType.PRESS,
            input=InputService.Mouse.LEFT,
        )

    def _handle_mouse_click(self, mouse_position: Vector2):
        if not self.is_point_inside(mouse_position):
            return

        self.on_click.fire()

    def _apply_size(self):
        super()._apply_size()
        self._rect.width = self._actual_size.x
        self._rect.height = self._actual_size.y

    def _apply_position(self):
        super()._apply_position()
        self._rect.x = self._actual_position.x
        self._rect.y = self._actual_position.y

    def draw(self):
        pyray.draw_rectangle_pro(
            self._rect,
            self._render_origin.to_tuple(),
            self._rotation,
            self._color.to_tuple(),
        )
