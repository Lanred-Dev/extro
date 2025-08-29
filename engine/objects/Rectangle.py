import pygame
from engine import engine
from engine.objects.BaseObject import BaseObject

class Rectangle(BaseObject):
    def __init__(self):
        super().__init__(self.__tick)
        
        self.color = pygame.Color(0, 0, 0)

    def __tick(self):
        pygame.draw.rect(engine.screen, self.color, (self.position.x, self.position.y, self.size.x, self.size.y))
