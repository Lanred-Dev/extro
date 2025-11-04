import pyray

import extro.internal.systems.UI as UISystem
from extro.instances.core.Instance.UI import UIInstance


class Frame(UIInstance):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(type=UISystem.UIInstanceType.GENERIC, **kwargs)

    def draw(self):
        pyray.draw_rectangle_pro(
            (*self.transform._actual_position, *self.transform._actual_size),
            self.transform._position_offset,
            self.transform._rotation,
            self.drawable.color.to_tuple(),
        )
