from typing import Generic, TYPE_CHECKING
from copy import deepcopy
from enum import Enum
from src.animation.lerp import lerp, LerpableType
from src.animation.easings import easings
from src.internal.components.Signal import Signal
from src.internal.components.Janitor import Janitor
from src.internal.Engine import Engine
from src.internal.Console import Console, LogType
from src.shared_types import EasingFunction

if TYPE_CHECKING:
    from . import LerpableType


class TweenState(Enum):
    """Represents the playback state of a tween."""

    PLAYING = 1
    PAUSED = 2
    STOPPED = 3


class Tween(Generic[LerpableType]):
    """
    Handles interpolation (tweening) between two values over time.

    Attributes
    ----------
    start : LerpableType
        Starting value of the tween.
    end : LerpableType
        Target value of the tween.
    value : LerpableType
        Current interpolated value.
    progress : float
        Progress from 0.0 to 1.0.
    duration : float
        Duration of the tween in seconds.
    easing : EasingFunction
        Easing function used for interpolation.
    """

    start: LerpableType
    end: LerpableType
    value: LerpableType
    progress: float
    duration: float
    easing: EasingFunction

    __elapsed: float
    __state: TweenState
    __on_pre_render_connection: str | None
    __janitor: Janitor

    on_play: Signal
    on_complete: Signal
    on_update: Signal

    def __init__(self, start: LerpableType, end: LerpableType):
        """Initialize a tween from start to end values."""
        self.start = start
        self.end = end
        self.value = deepcopy(start)
        self.progress = 0
        self.duration = 1
        self.easing = easings["linear"]

        self.__elapsed = 0
        self.__state = TweenState.STOPPED
        self.__on_pre_render_connection = None

        self.on_play = Signal()
        self.on_complete = Signal()
        self.on_update = Signal()

        self.__janitor = Janitor()
        self.__janitor.add(self.stop)
        self.__janitor.add(self.on_play)
        self.__janitor.add(self.on_complete)
        self.__janitor.add(self.on_update)

    def destroy(self):
        """Clean up all connections and stop the tween."""
        self.__janitor.destroy()

    def play(self):
        """Start or resume the tween. Connects to the engine's pre-render event."""
        if self.__state == TweenState.PLAYING:
            Console.log(
                "Tween is already playing. If the intent is to restart use `restart()`.",
                LogType.WARNING,
            )
            return

        self.restart()
        self.__state = TweenState.PLAYING
        self.__on_pre_render_connection = Engine.on_pre_render.connect(self.__tick)

    def pause(self):
        """Pause the tween without resetting its progress."""
        self.__state = TweenState.PAUSED

    def stop(self):
        """Stop the tween and disconnect from the engine."""
        self.__state = TweenState.STOPPED

        if self.__on_pre_render_connection is not None:
            Engine.on_pre_render.disconnect(self.__on_pre_render_connection)
            self.__on_pre_render_connection = None

    def restart(self):
        """Restart the tween from the beginning."""
        self.__elapsed = 0
        self.progress = 0
        self.value = deepcopy(self.start)

    def __tick(self):
        """Internal method called every frame to update the tween."""
        if self.__state is not TweenState.PLAYING:
            return

        self.__elapsed += Engine.delta
        self.progress = self.easing(self.__elapsed / self.duration)
        self.__update_value()

        if self.__elapsed >= self.duration:
            self.__complete()

    def __complete(self):
        """Complete the tween, set progress to 1, and fire the completion signal."""
        self.progress = 1
        self.__state = TweenState.STOPPED
        self.__update_value()
        self.on_complete.fire()

    def __update_value(self):
        """Update the current value based on the start, end, and progress, then fire the update signal."""
        self.value = lerp(self.start, self.end, self.progress)
        self.on_update.fire()
