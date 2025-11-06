from typing import TYPE_CHECKING, Generic

from extro.instances.core.Instance import Instance
import extro.Console as Console
from extro.utils.Signal import Signal
import extro.internal.systems.Animation as AnimationSystem
from extro.animation.easings.linear import linear
from extro.animation.lerp import LerpableType

if TYPE_CHECKING:
    from extro.animation.easings.__easings__ import EasingFunction


class Tween(Instance, Generic[LerpableType]):
    __slots__ = Instance.__slots__ + (
        "value",
        "duration",
        "easing",
        "on_update",
        "on_finish",
        "progress",
        "start",
        "end",
        "_is_active",
        "elapsed",
    )

    value: LerpableType
    duration: float
    easing: "EasingFunction"
    on_update: Signal
    on_finish: Signal
    progress: float
    start: LerpableType
    end: LerpableType
    _is_active: bool
    elapsed: float

    def __init__(
        self,
        start: LerpableType,
        end: LerpableType,
        duration: float,
        easing: "EasingFunction" = linear,
    ):
        super().__init__()

        self.start = start
        self.end = end
        self.duration = duration
        self.easing = easing
        self._is_active = False
        self.elapsed = 0.0
        self.progress = 0.0

        self.on_update = Signal()
        self.on_finish = Signal()
        self._janitor.add(self.on_update)
        self._janitor.add(self.on_finish)

        AnimationSystem.tweens.register(self._id)
        self._janitor.add(AnimationSystem.tweens.unregister, self._id)

    def play(self, start: LerpableType | None = None, end: LerpableType | None = None):
        if self._is_active:
            Console.log(
                f"Cannot play tween {self._id} because its already playing",
                Console.LogType.WARNING,
            )
            return

        if start is not None:
            self.start = start

        if end is not None:
            self.end = end

        self.elapsed = 0.0
        self.value = self.start
        self._is_active = True

    def restart(self):
        if self._is_active:
            self.cancel()

        self.play()

    def cancel(self):
        if not self._is_active:
            Console.log(
                f"Cannot cancel tween {self._id} because its not playing",
                Console.LogType.WARNING,
            )
            return

        self._is_active = False

    @property
    def is_active(self) -> bool:
        return self._is_active
