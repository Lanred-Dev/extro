import pygame
from .Instance import Instance, RenderUpdateType
from engine import engine


class AdvancedInstance(Instance):
    """A instance that uses a surface for rendering."""

    def __init__(self):
        super().__init__()
        self.surface: pygame.Surface
        self.update_surface()

    def draw(self):
        engine.screen.blit(self.surface, self.actual_position)

    def update_render(self, type: RenderUpdateType):
        super().update_render(type)

        # For advanced positions everything is drawn onto a surface, which does not use the instance position.
        if type == RenderUpdateType.SIZE:
            self.update_surface()

    def update_surface(self):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
