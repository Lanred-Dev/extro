import time
import sys
import pyray

import src.internal.Renderer as Renderer
import src.internal.CollisionHandler as CollisionHandler
import src.internal.InstanceHandler as InstanceHandler
import src.internal.InputHandler as InputHandler
from src.internal.components.Signal import Signal
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

        InputHandler._update_inputs()
        InstanceHandler._update_instances()
        CollisionHandler._update_collisions()

        on_pre_render.fire()
        Renderer._render()
        on_post_render.fire()

    quit()


def quit():
    pyray.close_window()
    sys.exit()


__all__ = ["start", "quit", "delta", "on_pre_render", "on_post_render"]
