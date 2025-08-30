import pygame
from engine import engine
from engine.instances import Rectangle
from engine.components import Signal


class Button(Rectangle):
    def __init__(self):
        super().__init__()
        self.janitor.add(
            engine.on_click.disconnect, engine.on_click.connect(self.___handle_click)
        )
        self.on_click: Signal = Signal()
        self.janitor.add(self.on_click)

    def ___handle_click(self, event: pygame.event.Event):
        mouseX: float = event.pos[0]
        mouseY: float = event.pos[1]

        if (
            mouseX >= self.actual_position.x
            and mouseX <= self.actual_position.x + self.size.x
            and mouseY >= self.actual_position.y
            and mouseY <= self.actual_position.y + self.size.y
        ):
            self.on_click.fire(event)
