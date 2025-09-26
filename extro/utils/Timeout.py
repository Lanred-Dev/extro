import extro.services.Render as RenderService
from extro.utils.Signal import Signal
import extro.internal.Engine as Engine


class Timeout:
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

    delay: float
    on_finish: Signal
    _running: bool
    _elapsed: float
    _engine_post_render_connection: str

    def __init__(self, delay: float):
        self.delay = delay
        self.on_finish = Signal()
        self._running = False
        self._elapsed = 0.0
        self._engine_post_render_connection = RenderService.on_post_render.connect(
            self._update
        )

    def destroy(self):
        RenderService.on_post_render.disconnect(self._engine_post_render_connection)
        self.on_finish.destroy()

    def start(self):
        """Start the timeout. If it is already running, it will be restarted."""
        self._elapsed = 0.0
        self._running = True

    def cancel(self):
        """Cancel the timeout if it is running."""
        if not self._running:
            return

        self._running = False

    def _update(self):
        if not self._running:
            return

        self._elapsed += Engine.delta

        if self._elapsed >= self.delay:
            self._finish()

    def _finish(self):
        self._running = False
        self.on_finish.fire()
