import pygame
from engine import engine
from .Instance import Instance


class Rectangle(Instance):
    """A drawable rectangle instance."""

    def draw(self):
        pygame.draw.rect(
            engine.screen,
            self.color,
            (self.actual_position.x, self.actual_position.y, self.size.x, self.size.y),
        )
