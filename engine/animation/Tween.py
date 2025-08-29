from typing import Callable, Any
import pygame
from engine import engine
from enum import Enum
from engine.utils.id import generateID
from engine.Signal import Signal
from engine.animation.lerpers import lerpColor, lerpNumber


class TweenState(Enum):
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3


class Tween:
    id: str
    start: float | pygame.Color | pygame.Vector2
    end: float | pygame.Color | pygame.Vector2
    value: Any
    progress: float
    duration: float
    easing: Callable[[float], float]
    __elapsed: float
    __state: TweenState
    onComplete: Signal

    def __init__(self):
        self.id = generateID(8)
        self.start = 0
        self.end = 0
        self.progress = 0
        self.duration = 1
        self.easing = lambda t: t
        self.__elapsed = 0
        self.__state = TweenState.STOPPED
        self.onComplete = Signal()

    def __del__(self):
        self.stop()

    def play(self):
        self.restart()
        self.__state = TweenState.PLAYING
        engine.register_updater(self.id, self.__tick)

    def restart(self):
        if isinstance(self.start, pygame.Vector2):
            self.value = self.start.copy()
        elif isinstance(self.start, pygame.Color):
            self.value = pygame.Color(self.start)
        else:
            self.value = self.start

        self.__elapsed = 0
        self.progress = 0

    def pause(self):
        self.__state = TweenState.PAUSED

    def stop(self):
        self.__state = TweenState.STOPPED
        engine.unregister_updater(self.id)

    def __complete(self):
        self.stop()
        self.progress = 1
        self.__update()
        self.onComplete.fire()

    def __update(self):
        if isinstance(self.start, pygame.Vector2) and isinstance(
            self.end, pygame.Vector2
        ):
            self.value.x = lerpNumber(self.start.x, self.end.x, self.progress)
            self.value.y = lerpNumber(self.start.y, self.end.y, self.progress)
        elif isinstance(self.start, pygame.Color) and isinstance(
            self.end, pygame.Color
        ):
            [r, g, b, a] = lerpColor(self.start, self.end, self.progress)
            self.value.r = r
            self.value.g = g
            self.value.b = b
            self.value.a = a
        elif isinstance(self.start, (float, int)) and isinstance(
            self.end, (float, int)
        ):
            self.value = lerpNumber(float(self.start), float(self.end), self.progress)

    def __tick(self):
        if self.__state != TweenState.PLAYING:
            return

        self.__elapsed += engine.delta
        self.progress = self.easing(min(self.__elapsed / self.duration, 1))
        self.__update()

        if self.__elapsed >= self.duration:
            self.__complete()
