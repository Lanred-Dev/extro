# python -m tests.proximity_area

import src as extro

extro.Renderer.set_fps(60)
extro.WorldService.set_world_tile_size(100)
extro.Window.set_title("Proximity Area Test")


def on_enter(instance):
    print(f"Entered proximity area: {instance.id}")
    instance.color = extro.Color(0, 255, 0)


def on_exit(instance):
    print(f"Exited proximity area: {instance.id}")
    instance.color = extro.Color(255, 0, 0)


scene = extro.Instances.Scene()

rect1 = extro.Instances.world.Rectangle(
    color=extro.Color(255, 0, 0),
    size=extro.Vector2(2, 2),
    position=extro.Vector2(0, 0),
)
rect1.add_collider()
scene.add(rect1)

proximity_area = extro.Instances.world.ProximityArea(
    size=extro.Vector2(2, 2),
    position=extro.Vector2(0, 0),
)
proximity_area.on_enter.connect(on_enter)
proximity_area.on_exit.connect(on_exit)

debug_box = extro.Instances.world.Rectangle(
    color=extro.Color(0, 0, 255, 100),
    size=proximity_area.size,
    position=proximity_area.position,
)
scene.add(debug_box)


def on_mouse_move(position: extro.Vector2):
    rect1.position = position


extro.InputService.on_mouse_event.connect(
    on_mouse_move,
    extro.InputService.InputSignalConnectionType.ACTIVE,
    extro.InputService.Mouse.MOVE,
)

extro.Engine.start()
