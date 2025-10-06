import pyray

from extro.instances.core.Instance.UI import UIInstance
from extro.utils.Signal import Signal
import extro.internal.systems.UI as UISystem


class Button(UIInstance):
    __slots__ = ("on_click",)

    on_click: Signal

    def __init__(self, **kwargs):
        super().__init__(type=UISystem.UIInstanceType.BUTTON, **kwargs)

        self.on_click = Signal()
        self._janitor.add(self.on_click)

    def draw(self):
        pyray.draw_rectangle_pro(
            (*self.transform._actual_position, *self.transform._actual_size),
            self.transform._position_offset,
            self.transform._rotation,
            self.drawable.color.to_tuple(),
        )
