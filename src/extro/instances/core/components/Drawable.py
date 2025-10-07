from typing import TYPE_CHECKING

from extro.instances.core.components.Component import Component
from extro.shared.RGBAColorC import RGBAColor
import extro.internal.ComponentManager as ComponentManager

if TYPE_CHECKING:
    from extro.shared.types import EmptyFunction
    from extro.internal.InstanceManager import InstanceIDType


class Drawable(Component):
    __slots__ = Component.__slots__ + (
        "color",
        "_zindex",
        "is_visible",
        "_render_command",
    )

    _key = "drawable"

    color: RGBAColor
    _zindex: int
    is_visible: bool
    _render_command: "EmptyFunction"

    def __init__(
        self,
        owner: "InstanceIDType",
        render_command: "EmptyFunction",
        color: RGBAColor = RGBAColor(255, 255, 255),
        zindex: int = 0,
        is_visible: bool = True,
    ):
        super().__init__(owner, ComponentManager.ComponentType.DRAWABLE)

        self._render_command = render_command
        self.color = color
        self._zindex = zindex
        self.is_visible = is_visible

    @property
    def zindex(self) -> int:
        return self._zindex

    @zindex.setter
    def zindex(self, zindex: int):
        self._zindex = zindex
