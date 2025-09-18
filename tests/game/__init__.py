# python -m tests.game

"""
coin sprite: https://opengameart.org/content/spinning-gold-coin
"""

import random
import src as extro

extro.Renderer.set_fps(60)
extro.Window.set_title("Game Test")

coins: int = 0

ui = extro.Instances.Scene(type=extro.Renderer.RenderTargetType.INDEPENDENT)
coins_label = extro.Instances.ui.Text(
    text=f"{coins} coins",
    font_size=25,
    position=extro.Vector2(0.5, 0.05),
    anchor=extro.Vector2(0.5, 0.5),
)
ui.add(coins_label)

scene = extro.Instances.Scene()

character = extro.Instances.world.Sprite(
    image_path="tests/game/character_sprite.png",
    is_animated=True,
    frame_size=extro.Vector2(16, 11),
    frame_time=0.1,
    starting_frame=0,
    size=extro.Vector2(2, 1.375),
    position=extro.Vector2(3, 3),
)
character.add_physics_body(mass=0.1)
character.add_collider()
scene.add(character)


def on_key_down(key: extro.InputService.Key):
    match key:
        case extro.InputService.Key.A:
            character.physics_body.velocity.x = -70
        case extro.InputService.Key.D:
            character.physics_body.velocity.x = 70
        case extro.InputService.Key.W:
            character.physics_body.velocity.y = -70
        case extro.InputService.Key.S:
            character.physics_body.velocity.y = 70

    character.is_animated = character.physics_body.velocity.magnitude() > 0


def on_key_up(key: extro.InputService.Key):
    if not extro.InputService.is_input_active(
        extro.InputService.Key.A
    ) and not extro.InputService.is_input_active(extro.InputService.Key.D):
        character.physics_body.velocity.x = 0

    if not extro.InputService.is_input_active(
        extro.InputService.Key.W
    ) and not extro.InputService.is_input_active(extro.InputService.Key.S):
        character.physics_body.velocity.y = 0

    character.is_animated = character.physics_body.velocity.magnitude() > 0

    if not character.is_animated:
        character.current_frame = 0


extro.InputService.on_key_event.connect(
    on_key_down, extro.InputService.InputSignalConnectionType.PRESS
)
extro.InputService.on_key_event.connect(
    on_key_up, extro.InputService.InputSignalConnectionType.RELEASE
)


def on_coin_collision(
    coin: extro.Instances.world.Sprite, other: extro.Instances.world.Sprite
):
    global coins

    if other == character:
        coin.destroy()
        coins += 1
        coins_label.text = f"{coins} coins"


def spawn_coin():
    screen_size = extro.ScreenService.screen_size
    random_position = extro.ScreenService.screen_to_world_coords(
        extro.Vector2(
            random.uniform(0, screen_size.x),
            random.uniform(0, screen_size.y),
        )
    )

    coin = extro.Instances.world.Sprite(
        image_path="tests/game/coin_sprite.png",
        is_animated=True,
        frame_size=extro.Vector2(32, 32),
        frame_time=0.1,
        starting_frame=0,
        size=extro.Vector2(1, 1),
        position=random_position,
    )
    coin.add_collider()
    coin.collider.on_collision.connect(lambda other: on_coin_collision(coin, other))
    scene.add(coin)


# set a timeout
coin_timeout = extro.Timeout(2)


def handle_coin_timeout():
    spawn_coin()
    coin_timeout.start()


coin_timeout.on_finish.connect(handle_coin_timeout)
coin_timeout.start()
extro.Engine.start()
