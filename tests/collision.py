# python -m tests.collision

import src as extro

extro.Renderer.set_fps(60)
extro.Renderer.set_world_tile_size(100)
extro.Window.title = "Collision Test"


def on_rect1_collision(other):
    rect1.color = extro.Color(0, 255, 0)


def on_rect1_collision_end(other):
    rect1.color = extro.Color(255, 0, 0)


def on_rect2_collision(other):
    rect2.color = extro.Color(0, 255, 0)


def on_rect2_collision_end(other):
    rect2.color = extro.Color(255, 0, 0)


scene = extro.Instances.Scene()

rect1 = extro.Instances.world.Rectangle()
rect1.color = extro.Color(255, 0, 0)
rect1.size = extro.Vector2(2, 2)
rect1.position = extro.Vector2(0, 0)
rect1.on_collision.connect(on_rect1_collision)
rect1.on_collision_end.connect(on_rect1_collision_end)
scene.add_instance(rect1)

rect2 = extro.Instances.world.Rectangle()
rect2.color = extro.Color(255, 0, 0)
rect2.size = extro.Vector2(2, 2)
rect2.on_collision.connect(on_rect2_collision)
rect2.on_collision_end.connect(on_rect2_collision_end)
rect2.anchor = extro.Vector2(0.5, 0.5)
scene.add_instance(rect2)


def rotate_rect1():
    rect1.rotation += 1

    if rect1.rotation >= 360:
        rect1.rotation = 0


def on_mouse_move(position: extro.Vector2):
    rect2.position = position


extro.InputHandler.on_mouse_event.connect(
    on_mouse_move,
    extro.InputHandler.InputSignalConnectionType.ACTIVE,
    extro.InputHandler.Mouse.MOVE,
)

extro.Engine.on_pre_render.connect(rotate_rect1)
extro.Engine.start()
