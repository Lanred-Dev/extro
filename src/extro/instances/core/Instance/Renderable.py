from extro.instances.core.Instance import Instance
from extro.shared.RGBAColor import RGBAColor
from extro.shared.Coord import Coord
from extro.shared.Vector2 import Vector2
from extro.instances.core.components.Drawable import Drawable
from extro.instances.core.components.Transform import Transform
from extro.instances.core.components.Hierarchy import Hierarchy


class Renderable(Instance):
    __slots__ = Instance.__slots__ + ("drawable", "transform", "hierarchy")

    drawable: "Drawable"
    transform: "Transform"
    hierarchy: "Hierarchy"

    def __init__(
        self,
        position: Coord,
        size: Coord,
        color: RGBAColor = RGBAColor(255, 255, 255),
        zindex: int = 0,
        is_visible: bool = True,
        anchor: Vector2 = Vector2(0, 0),
        scale: Vector2 = Vector2(1, 1),
        rotation: float = 0,
    ):
        super().__init__()

        transform: Transform = Transform(
            self._id,
            position=position,
            size=size,
            anchor=anchor,
            scale=scale,
            rotation=rotation,
        )
        self.add_component(transform)
        self.transform = transform

        drawable: Drawable = Drawable(
            self._id,
            render_command=self.draw,
            color=color,
            zindex=zindex,
            is_visible=is_visible,
        )
        self.add_component(drawable)
        self.drawable = drawable

        hierarchy: Hierarchy = Hierarchy(self._id)
        self.add_component(hierarchy)
        self.hierarchy = hierarchy

    def draw(self):
        raise NotImplementedError("`draw` method must be implemented by subclass")
