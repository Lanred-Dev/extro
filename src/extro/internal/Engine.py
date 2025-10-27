import sys
import pyray
import time
from typing import TYPE_CHECKING

import extro.internal.systems.Render as RenderSystem
import extro.internal.systems.Input as InputSystem
import extro.internal.systems.Transform as TransformSystem
import extro.internal.systems.Audio as AudioSystem
import extro.internal.systems.Animation as AnimationSystem
import extro.internal.systems.UI as UISystem
import extro.internal.systems.Collision as CollisionSystem
import extro.internal.systems.Physics as PhysicsSystem
import extro.internal.systems.Timing as TimingSystem
import extro.Window as Window
import extro.Profiler as Profiler

if TYPE_CHECKING:
    from extro.shared.types import EmptyFunction


def run_system(update: "EmptyFunction", system_name: str):
    started = time.time()
    update()
    Profiler._add_update(system_name, time.time() - started)


def start():
    while not pyray.window_should_close():
        # The order matters, aka dont change it :)
        run_system(TimingSystem.update, "timing")
        run_system(InputSystem.update, "input")
        run_system(TransformSystem.update, "transform")
        run_system(
            UISystem.update, "ui"
        )  # If any transform changes happen because of UI events, they will be applied next frame
        run_system(CollisionSystem.update, "collision")
        run_system(PhysicsSystem.update, "physics")
        run_system(AnimationSystem.update, "animation")
        run_system(RenderSystem.render, "render")
        run_system(AudioSystem.update, "audio")

    quit()


def quit():
    AudioSystem.quit()
    Window.close()
    sys.exit()


__all__ = ["start", "quit"]
