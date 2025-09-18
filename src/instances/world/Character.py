import pyray
import time

from src.instances.world.Sprite import Sprite
from src.values.Vector2 import Vector2
import src.internal.Console as Console
import src.internal.Engine as Engine


class Character(Sprite):
    _speed: float

    def __init__(self, speed: float = 0.1, **kwargs):
        super().__init__(**kwargs)
        self._speed = speed

        self._janitor.add(
            Engine.on_pre_render.disconnect,
            Engine.on_pre_render.connect(self._update_velocity),
        )

    def move_in_direction(self, direction: Vector2):
        if direction.x == 0 and direction.y == 0:
            return

        direction = direction.normalized()
        self.position += direction * self._speed

    def _update_velocity(self):
        pass

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = speed
