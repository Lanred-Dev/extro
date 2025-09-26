# python -m examples.game

"""
coin sprite: https://opengameart.org/content/spinning-gold-coin
"""

import extro as extro

extro.services.RenderService.set_fps(144)
extro.Window.set_title("Game Test")
# extro.Console.set_log_priority(extro.Console.LogPriority.WARNING)
# extro.Window.toggle_fullscreen()

coins: int = 0

extro.services.InputService.register_action(
    "move.left", extro.services.InputService.Key.A
)
extro.services.InputService.register_action(
    "move.right", extro.services.InputService.Key.D
)
extro.services.InputService.register_action(
    "move.up", extro.services.InputService.Key.W
)
extro.services.InputService.register_action(
    "move.down", extro.services.InputService.Key.S
)

ui = extro.Instances.Scene(
    type=extro.services.RenderService.RenderTargetType.INDEPENDENT
)
coins_label = extro.Instances.ui.Text(
    text=f"{coins} coins",
    font_size=25,
    position=extro.Coord(0.5, 0.05, extro.CoordType.NORMALIZED),
    anchor=extro.Vector2(0.5, 0.5),
)
ui.add(coins_label)

SPEED_UPGRADE_COST: int = 50

camera = extro.Instances.world.TargetCamera()
extro.services.WorldService.set_camera(camera)

speed_upgrade_button = extro.Instances.ui.Button(
    position=extro.Coord(0.5, 0.95, extro.CoordType.NORMALIZED),
    anchor=extro.Vector2(0.5, 1),
    size=extro.Coord(0.5, 0.05, extro.CoordType.NORMALIZED),
    color=extro.Color(100, 100, 100),
)
ui.add(speed_upgrade_button)
speed_upgrade_text_label = extro.Instances.ui.Text(
    text=f"Speed +25 ({SPEED_UPGRADE_COST} coins)",
    font=extro.Instances.ui.Fonts.Arial,
    font_size=20,
    character_spacing=2,
    color=extro.Color(255, 255, 255),
    position=extro.Coord(0.5, 0.5, extro.CoordType.PARENT),
    anchor=extro.Vector2(0.5, 0.5),
)
speed_upgrade_button.add_child(speed_upgrade_text_label)
speed_upgrade_button.on_click.connect(lambda: upgrade_speed())


def upgrade_speed():
    global coins

    if coins >= SPEED_UPGRADE_COST:
        character.speed += 25
        coins -= SPEED_UPGRADE_COST
        coins_label.text = f"{coins} coins"


scene = extro.Instances.Scene()

character = extro.Instances.world.PlayableCharacter(
    image_file="examples/game/character_sprite.png",
    frame_size=extro.Vector2(16, 11),
    speed=60,
    size=extro.Coord(2, 1.375, extro.CoordType.WORLD),
)
scene.add(character)
camera.bind_to(character)

coin_count: int = 0


def update_speed_upgrade_button():
    if coins >= SPEED_UPGRADE_COST:
        speed_upgrade_button.color = extro.Color(0, 200, 0)
        speed_upgrade_text_label.color = extro.Color(255, 255, 255)
    else:
        speed_upgrade_button.color = extro.Color(100, 100, 100)
        speed_upgrade_text_label.color = extro.Color(150, 150, 150)


def on_coin_collision(
    coin: extro.Instances.world.Sprite, other: extro.Instances.world.Sprite
):
    global coins, coin_count

    if other == character:
        coin.destroy()
        coins += 1
        coin_count -= 1
        coins_label.text = f"{coins} coins"
        update_speed_upgrade_button()


def spawn_coin():
    global coin_count
    if coin_count >= 200:
        return
    coin_count += 1
    (random_x, random_y) = extro.services.ScreenService.random_world_coords()
    random_position = extro.Coord(
        random_x,
        random_y,
        extro.CoordType.WORLD,
    )

    coin = extro.Instances.world.AnimatedSprite(
        image_file="examples/game/coin_sprite.png",
        frame_size=extro.Vector2(32, 32),
        frame_duration=0.1,
        size=extro.Coord(1, 1, extro.CoordType.WORLD),
        position=random_position,
    )
    coin.add_collider()
    coin.collider.on_collision.connect(lambda other: on_coin_collision(coin, other))
    scene.add(coin)


coin_timeout = extro.utils.Timeout(0.005)


def handle_coin_timeout():
    spawn_coin()
    coin_timeout.start()


coin_timeout.on_finish.connect(handle_coin_timeout)
coin_timeout.start()
extro.Engine.start()
