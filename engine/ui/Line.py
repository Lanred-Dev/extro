import pygame
from engine import engine


class Line:
    """A drawable line instance."""

    def __init__(self):
        self.id = engine.create_instance_id()
        self.color: pygame.Color = pygame.Color(255, 255, 255)
        self.width: int = 1
        self.position_1: pygame.Vector2 = pygame.Vector2(0, 0)
        self.position_2: pygame.Vector2 = pygame.Vector2(0, 0)

    def init(self):
        engine.register_instance(self.id, self)

    def destroy(self):
        """Destroys the line."""
        engine.unregister_instance(self.id)

    def tick(self):
        pygame.draw.line(
            engine.screen, self.color, self.position_1, self.position_2, self.width
        )
