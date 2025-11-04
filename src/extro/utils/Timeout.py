from extro.utils.Signal import Signal
import extro.internal.systems.Timing as TimingSystem
from extro.instances.core.Instance import Instance
import extro.Console as Console


class Timeout(Instance):
    """
    A simple timeout class that fires a signal after a delay. Can be reused.

    Example
    -------
    >>> timeout = extro.Timeout(2)  # 2 seconds
    >>> timeout.on_finish.connect(lambda: print("Timeout finished!"))
    >>> timeout.start()

    Once you are finished with the timeout:
    >>> timeout.destroy()
    """

    __slots__ = (
        "delay",
        "on_finish",
        "is_active",
        "elapsed",
    )

    delay: float
    on_finish: Signal
    is_active: bool
    elapsed: float

    def __init__(self, delay: float):
        super().__init__()

        self.delay = delay
        self.on_finish = Signal()
        self._janitor.add(self.on_finish)
        self.is_active = False
        self.elapsed = 0.0

        TimingSystem.timeouts.register(self._id)
        self._janitor.add(TimingSystem.timeouts.unregister, self._id)

    def start(self):
        if self.is_active:
            Console.log(
                f"Cannot start timeout {self._id} because its already active",
                Console.LogType.WARNING,
            )
            return

        self._elapsed = 0.0
        self.is_active = True

    def restart(self):
        if self.is_active:
            self.cancel()

        self.start()

    def cancel(self):
        if not self.is_active:
            Console.log(
                f"Cannot cancel timeout {self._id} because its not active",
                Console.LogType.WARNING,
            )
            return

        self.is_active = False
