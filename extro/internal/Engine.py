import sys
import pyray
import time
from typing import TYPE_CHECKING

import extro.internal.systems.Render as RenderSystem
import extro.internal.systems.Collision as CollisionSystem
import extro.internal.InstanceManager as InstanceManager
import extro.internal.systems.Input as InputSystem
import extro.internal.systems.Audio as AudioSystem
import extro.internal.systems.Physics as PhysicsSystem
import extro.internal.systems.Animation as AnimationSystem
import extro.Window as Window
import extro.Profiler as Profiler

if TYPE_CHECKING:
    from extro.shared.types import EmptyFunction

delta: float = 0


def run_system(update: "EmptyFunction", system_name: str):
    """Run the system and log its execution time to the profiler."""
    started = time.time()
    update()
    Profiler._add_update(system_name, time.time() - started)


def start():
    global delta

    while not pyray.window_should_close():
        delta = pyray.get_frame_time()

        # The order matters, aka dont change it :)
        run_system(InputSystem.update_inputs, "input")
        run_system(InstanceManager.update_queued, "instance")
        run_system(AudioSystem.update, "audio")
        run_system(PhysicsSystem.update, "physics")
        run_system(CollisionSystem.check_collisions, "collision")
        run_system(AnimationSystem.update, "animation")
        run_system(RenderSystem.render, "render")

    quit()


def quit():
    AudioSystem.quit()
    Window.close()
    sys.exit()


__all__ = ["start", "quit", "delta"]
