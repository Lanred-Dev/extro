from typing import TYPE_CHECKING

import pyray

import extro.Console as Console
import extro.internal.InstanceManager as InstanceManager

if TYPE_CHECKING:
    from extro.instances.world.Sprite.Animated import AnimatedSprite

sprites: list[int] = []
tweens: list[str] = []


def register_sprite(sprite_id: int):
    if sprite_id in sprites:
        Console.log(
            f"Sprite {sprite_id} is already registered", Console.LogType.WARNING
        )
        return

    sprites.append(sprite_id)
    Console.log(f"Sprite {sprite_id} registered")


def unregister_sprite(sprite_id: int):
    if sprite_id not in sprites:
        Console.log(f"Sprite {sprite_id} is not registered", Console.LogType.WARNING)
        return

    sprites.remove(sprite_id)
    Console.log(f"Sprite {sprite_id} unregistered")


def update():
    current_time: float = pyray.get_time()

    for sprite_id in sprites:
        sprite: "AnimatedSprite" = InstanceManager.instances[sprite_id]  # type: ignore

        if (
            not sprite._is_active
            or current_time - sprite._last_frame_at < sprite._frame_duration
        ):
            continue

        sprite._current_frame.x = (sprite._current_frame.x + 1) % sprite._frame_count
        sprite._texture_source.x = sprite._current_frame.x * sprite._source_size.x
        sprite._texture_source.y = sprite._current_frame.y * sprite._source_size.y
        sprite._last_frame_at = current_time
