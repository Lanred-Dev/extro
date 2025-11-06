import sys
import pyray
import time
from typing import Callable, Any, TYPE_CHECKING

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
    AnyFunction = Callable[..., Any]


def run_system(update: "AnyFunction", system_name: str, *args: Any) -> Any:
    started = time.time()
    result = update(*args)
    Profiler.capture(system_name, time.time() - started)
    return result


def start():
    while not pyray.window_should_close():
        # The order matters, aka dont change it :)
        run_system(TimingSystem.update, "timing")
        run_system(InputSystem.update, "input")
        run_system(TransformSystem.update, "transform")

        collisions_data: "CollisionSystem.CollisionsData" = run_system(
            CollisionSystem.update, "collision"
        )
        run_system(PhysicsSystem.update, "physics", collisions_data)

        # If any transform changes happen because of UI events, they will be applied next frame
        run_system(UISystem.update, "ui")
        run_system(AnimationSystem.update, "animation")
        run_system(RenderSystem.render, "render")
        run_system(AudioSystem.update, "audio")

    quit()


def quit():
    AudioSystem.quit()
    Window.close()
    sys.exit()


__all__ = ["start", "quit"]
