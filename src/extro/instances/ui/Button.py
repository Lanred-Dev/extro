import pyray

from extro.instances.core.Instance.UI.Clickable import Clickable


class Button(Clickable):
    def draw(self):
        pyray.draw_rectangle_pro(
            self.transform._bounding,
            self.transform._position_offset,
            self.transform.rotation,
            self.drawable.color.list,
        )
