from extro.instances.core.Instance.UI import UIInstance
from extro.utils.Signal import Signal
import extro.internal.systems.UI as UISystem


class Clickable(UIInstance):
    __slots__ = ("on_click",)

    on_click: Signal

    def __init__(self, **kwargs):
        super().__init__(type=UISystem.UIInstanceType.CLICKABLE, **kwargs)

        self.on_click = Signal()
        self._janitor.add(self.on_click)
