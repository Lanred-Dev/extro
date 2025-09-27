import pyray

from extro.core.Instance.UI import UIInstance
from extro.utils.Signal import Signal
import extro.internal.systems.UI as UISystem


class Button(UIInstance):
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

        UISystem.register(self._id, UISystem.UIInstanceType.BUTTON)
        self._janitor.add(UISystem.unregister, self._id)

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
