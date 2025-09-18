# python -m tests.collision

import src as extro

extro.Renderer.set_fps(60)
extro.Window.set_title("Collision Test")
extro.WorldService.set_world_tile_size(100)


def on_rect1_collision(other):
    rect1.color = extro.Color(0, 255, 0)


def on_rect1_collision_end(other):
    rect1.color = extro.Color(255, 0, 0)


def on_rect2_collision(other):
    rect2.color = extro.Color(0, 255, 0)


def on_rect2_collision_end(other):
    rect2.color = extro.Color(255, 0, 0)


scene = extro.Instances.Scene()

rect1 = extro.Instances.world.Rectangle(
    color=extro.Color(255, 0, 0),
    size=extro.Vector2(2, 2),
    position=extro.Vector2(0, 0),
)
rect1.add_collider()
rect1.collider.on_collision.connect(on_rect1_collision)
rect1.collider.on_collision_end.connect(on_rect1_collision_end)
scene.add(rect1)

rect2 = extro.Instances.world.Rectangle(
    color=extro.Color(255, 0, 0),
    size=extro.Vector2(1, 1),
)
rect2.add_collider()
rect2.collider.on_collision.connect(on_rect2_collision)
rect2.collider.on_collision_end.connect(on_rect2_collision_end)
scene.add(rect2)


def rotate_rect1():
    rect1.rotation += 1

    if rect1.rotation >= 360:
        rect1.rotation = 0


def increase_rect2_size():
    rect2.size += extro.Vector2(0.2, 0.2)


def decrease_rect2_size():
    rect2.size -= extro.Vector2(0.2, 0.2)


def on_mouse_move(position: extro.Vector2):
    rect2.position = extro.ScreenService.screen_to_world_coords(position)


extro.InputService.on_mouse_event.connect(
    on_mouse_move,
    extro.InputService.InputSignalConnectionType.ACTIVE,
    extro.InputService.Mouse.MOVE,
)

extro.InputService.on_key_event.connect(
    increase_rect2_size,
    extro.InputService.InputSignalConnectionType.PRESS,
    extro.InputService.Key.E,
)

extro.InputService.on_key_event.connect(
    decrease_rect2_size,
    extro.InputService.InputSignalConnectionType.PRESS,
    extro.InputService.Key.Q,
)

extro.Engine.on_pre_render.connect(rotate_rect1)
extro.Engine.start()
