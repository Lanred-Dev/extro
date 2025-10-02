from extro.instances.core.Instance import Instance
from extro.shared.RGBAColorC import RGBAColor
from extro.shared.Coord import Coord
from extro.shared.Vector2C import Vector2
from extro.instances.core.components.Drawable import Drawable
from extro.instances.core.components.Transform import Transform


class Renderable(Instance):
    drawable: "Drawable"
    transform: "Transform"

    def __init__(
        self,
        position: Coord,
        size: Coord,
        color: RGBAColor = RGBAColor(255, 255, 255),
        zindex: int = 0,
        is_visible: bool = True,
        anchor: Vector2 = Vector2(0, 0),
        scale: Vector2 = Vector2(1, 1),
    ):
        super().__init__()

        self.add_component(
            "transform",
            Transform(
                self.id, position=position, size=size, anchor=anchor, scale=scale
            ),
        )
        self.transform = self.get_component_unsafe("transform")

        self.add_component(
            "drawable",
            Drawable(
                self.id,
                render_command=self.draw,
                color=color,
                zindex=zindex,
                is_visible=is_visible,
            ),
        )
        self.drawable = self.get_component_unsafe("drawable")

    def draw(self):
        raise NotImplementedError("`draw` method must be implemented by subclass")
