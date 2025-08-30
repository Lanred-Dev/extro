from .CollisionInstance import CollisionInstance
from .Instance import RenderUpdateType
import pygame


class Part(CollisionInstance):
    def update_render(self, type: RenderUpdateType):
        super().update_render(type)

        if type != RenderUpdateType.POSITION:
            pygame.draw.rect(
                self.surface,
                self.color,
                (0, 0, self.size.x, self.size.y),
            )

        if type == RenderUpdateType.SIZE:
            self.update_collision_mask()
