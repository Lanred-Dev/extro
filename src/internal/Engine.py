import time
import sys
import pyray

import src.internal.handlers.Renderer as Renderer
import src.internal.handlers.CollisionHandler as CollisionHandler
import src.internal.handlers.InstanceManager as InstanceManager
import src.internal.services.InputService as InputService
import src.internal.Window as Window
import src.internal.handlers.PhysicsHandler as PhysicsHandler
from src.internal.helpers.Signal import Signal
from src.__version__ import __version__

delta: float = 0
_last_frame_at: float = time.perf_counter()
on_pre_render: Signal = Signal()
on_post_render: Signal = Signal()


def start():
    global delta, _last_frame_at

    while not pyray.window_should_close():
        now: float = time.perf_counter()
        delta = now - _last_frame_at
        _last_frame_at = now

        InputService._update()
        InstanceManager._update()
        PhysicsHandler._update()
        CollisionHandler._update()

        on_pre_render.fire()
        Renderer._render()
        on_post_render.fire()

    quit()


def quit():
    Window._close()
    sys.exit()


__all__ = ["start", "quit", "delta", "on_pre_render", "on_post_render"]
