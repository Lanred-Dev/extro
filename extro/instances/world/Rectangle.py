import pyray

from extro.core.Instance.Drawable import DrawableInstance


class Rectangle(DrawableInstance):
    __slots__ = ("_rect",)

    _rect: pyray.Rectangle

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._rect = pyray.Rectangle(
            self._actual_position.x,
            self._actual_position.y,
            self._actual_size.x,
            self._actual_size.y,
        )

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
