import pyray
from typing import TYPE_CHECKING

import extro.services.Input as InputService
from extro.core.Instance.Drawable import DrawableInstance
from extro.utils.Signal import Signal

if TYPE_CHECKING:
    from extro.shared.Vector2 import Vector2


class Button(DrawableInstance):
    __slots__ = ("_rect", "on_click")

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

        self._janitor.add(
            InputService.on_mouse_event.disconnect,
            InputService.on_mouse_event.connect(
                self._handle_click,
                type=InputService.SubscriberType.PRESS,
                input=InputService.Mouse.LEFT,
            ),
        )

    def _handle_click(self, _, mouse_position: "Vector2"):
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
