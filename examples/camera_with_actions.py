import extro

extro.Services.RenderService.set_fps(60)
extro.Window.set_title("The cube moves... but with the camera")

SPEED: float = 100.0

camera: extro.Instances.Core.Camera = extro.Instances.Core.Camera()
scene = extro.Instances.World.Scene()

rect = extro.Instances.World.Rectangle(
    position=extro.Coord(0, 0, extro.Coord.CoordType.WORLD),
    size=extro.Coord(2, 2, extro.Coord.CoordType.WORLD),
    color=extro.RGBAColor(255, 0, 0),
)
scene.add(rect)


def update_camera():
    move_vector: extro.Vector2 = extro.Vector2(0, 0)

    if extro.Services.InputService.is_action_active("move_up"):
        move_vector.y -= 1
    elif extro.Services.InputService.is_action_active("move_down"):
        move_vector.y += 1

    if extro.Services.InputService.is_action_active("move_left"):
        move_vector.x -= 1
    elif extro.Services.InputService.is_action_active("move_right"):
        move_vector.x += 1

    camera.position = (
        camera.position + (move_vector * extro.Services.TimingService.delta) * SPEED
    )


extro.Services.InputService.register_action(
    "move_up",
    extro.Services.InputService.Keyboard.W,
)
extro.Services.InputService.register_action(
    "move_down",
    extro.Services.InputService.Keyboard.S,
)
extro.Services.InputService.register_action(
    "move_left",
    extro.Services.InputService.Keyboard.A,
)
extro.Services.InputService.register_action(
    "move_right",
    extro.Services.InputService.Keyboard.D,
)

extro.Services.WorldService.set_camera(camera)
extro.Services.TimingService.on_pre_render.connect(update_camera)

extro.Engine.start()
