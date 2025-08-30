import pygame
from engine.instances import Instance
from engine import engine

DEFAULT_FONT: pygame.font.Font = pygame.font.SysFont("Comic Sans MS", 30)


class Text(Instance):
    def __init__(self):
        super().__init__()
        self.text: str = "Hello World"
        self.font: pygame.font.Font = DEFAULT_FONT

    def predraw(self):
        super().predraw()
        text_surface = self.font.render(self.text, True, self.color)
        engine.screen.blit(text_surface, self.actual_position)
