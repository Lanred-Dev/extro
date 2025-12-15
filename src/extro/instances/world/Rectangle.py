import pyray

from extro.instances.core.Instance.Renderable import Renderable


class Rectangle(Renderable):
    def draw(self):
        pyray.draw_rectangle_pro(
            self.transform._bounding,
            self.transform._position_offset,
            self.transform.rotation,
            self.drawable.color.list,
        )
