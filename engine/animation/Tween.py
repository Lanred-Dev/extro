import typing
from enum import Enum
from engine.components import Signal, Janitor
from engine.animation.lerp import lerp, LerpableType
from engine.animation.easings import EasingFunction, linear
from engine.Console import console, LogType
from engine import engine
import copy


class TweenState(Enum):
    """Represents the playback state of a tween."""

    PLAYING = 1
    PAUSED = 2
    STOPPED = 3


class Tween(typing.Generic[LerpableType]):
    """A class for interpolating between two values over time."""

    def __init__(self, start: LerpableType, end: LerpableType):
        self.start: LerpableType = start
        self.end: LerpableType = end
        self.value: LerpableType = copy.deepcopy(start)
        self.progress: float = 0
        self.duration: float = 1
        self.easing: EasingFunction = linear

        self.__elapsed = 0
        self.__state: TweenState = TweenState.STOPPED
        self.__on_tick_connection: str | None = None
        self.__janitor: Janitor = Janitor()

        self.on_play: Signal = Signal()
        self.on_complete: Signal = Signal()
        self.on_update: Signal = Signal()

        self.__janitor.add(self.stop)
        self.__janitor.add(self.on_play)
        self.__janitor.add(self.on_complete)
        self.__janitor.add(self.on_update)

    def destroy(self):
        """Destroy the tween."""
        self.__janitor.destroy()

    def play(self):
        """Start or resume playback of the tween."""
        if self.__state == TweenState.PLAYING:
            console.log(
                "Tween is already playing. If the intent is to restart use `restart()`.",
                LogType.WARNING,
            )
            return

        self.restart()
        self.__state = TweenState.PLAYING
        self.__on_tick_connection = engine.on_tick.connect(self.__tick)

    def pause(self):
        """Pause the tween without resetting progress."""
        self.__state = TweenState.PAUSED

    def stop(self):
        """Stop the tween and disconnect it from updates."""
        self.__state = TweenState.STOPPED

        if self.__on_tick_connection is not None:
            engine.on_tick.disconnect(self.__on_tick_connection)
            self.__on_tick_connection = None

    def restart(self):
        """Reset tween progress and value, but do not play."""
        self.__elapsed = 0
        self.progress = 0
        self.value = copy.deepcopy(self.start)

    def __tick(self):
        """Advance tween progress on each engine tick."""
        if self.__state is not TweenState.PLAYING:
            return

        self.__elapsed += engine.delta
        self.progress = self.easing(self.__elapsed / self.duration)
        self.__update_value()

        if self.__elapsed >= self.duration:
            self.__complete()

    def __complete(self):
        """Mark the tween as complete and fire its completion signal."""
        self.progress = 1
        self.__update_value()
        self.on_complete.fire()

    def __update_value(self):
        """Recalculate the tweened value based on current progress."""
        self.value = lerp(self.start, self.end, self.progress)
        self.on_update.fire()
