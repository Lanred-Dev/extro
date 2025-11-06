import pyray

from extro.instances.core.Instance.Renderable import Renderable


class Rectangle(Renderable):
    def draw(self):
        pyray.draw_rectangle_pro(
            (*self.transform._actual_position, *self.transform._actual_size),
            self.transform._position_offset,
            self.transform._rotation,
            self.drawable.color.list,
        )
