import pygame
from engine.utils.id import generateID
from engine import engine
from typing import Callable


class BaseObject:
    id: str
    size: pygame.Vector2
    position: pygame.Vector2

    def __init__(self, updater: Callable[[], None]):
        self.id = generateID()
        self.size = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(0, 0)
        engine.register_updater(self.id, updater)

    def delete(self):
        engine.unregister_updater(self.id)

    def move(self, x: float, y: float):
        self.position.x += x
        self.position.y += y
