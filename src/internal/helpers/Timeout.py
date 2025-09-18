import src.internal.Engine as Engine
from src.internal.helpers.Signal import Signal


class Timeout:
    delay: float
    on_finish: Signal
    _running: bool
    _elapsed: float
    _engine_post_render_connection: str | None = None

    def __init__(self, delay: float):
        self.delay = delay
        self.on_finish = Signal()
        self._running = False
        self._elapsed = 0.0
        self._engine_post_render_connection = None

    def destroy(self):
        self.on_finish.destroy()
        self._disconnect_engine_post_render()

    def _update(self):
        if not self._running:
            return

        self._elapsed += Engine.delta

        if self._elapsed >= self.delay:
            self.on_finish.fire()
            self._disconnect_engine_post_render()

    def start(self):
        self._elapsed = 0.0
        self._running = True
        self._engine_post_render_connection = Engine.on_post_render.connect(
            self._update
        )

    def cancel(self):
        self._running = False
        self._disconnect_engine_post_render()

    def _disconnect_engine_post_render(self):
        if self._engine_post_render_connection is None:
            return

        Engine.on_post_render.disconnect(self._engine_post_render_connection)
        self._engine_post_render_connection = None
