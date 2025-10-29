from extro.instances.core.Instance.UI import UIInstance
from extro.utils.Signal import Signal
import extro.internal.systems.UI as UISystem


class Clickable(UIInstance):
    __slots__ = UIInstance.__slots__ + ("on_click", "on_focus", "on_focus_lost")

    on_click: Signal
    on_focus: Signal
    on_focus_lost: Signal

    def __init__(self, **kwargs):
        super().__init__(type=UISystem.UIInstanceType.CLICKABLE, **kwargs)

        self.on_click = Signal()
        self._janitor.add(self.on_click)
        self.on_focus = Signal()
        self._janitor.add(self.on_focus)
        self.on_focus_lost = Signal()
        self._janitor.add(self.on_focus_lost)
