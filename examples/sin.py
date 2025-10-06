import math
import extro

extro.Services.RenderService.set_fps(60)
extro.Services.WorldService.set_tile_size(100)
extro.Window.set_title("Animated sin wave")

scene = extro.Instances.world.Scene()

current_x = 0
rect = extro.Instances.world.Rectangle(
    position=extro.Coord(current_x, 0, extro.CoordType.ABSOLUTE),
    size=extro.Coord(15, 15, extro.CoordType.ABSOLUTE),
    color=extro.RGBAColor(255, 0, 0),
)
scene.add(rect)

amplitude: int = 100
frequency: float = 0.1


def next_frame():
    global current_x

    if current_x >= extro.Window.size.x:
        current_x = 0

    current_x += 1
    y = math.sin(current_x * frequency) * amplitude + (extro.Window.size.y / 2)
    rect.transform.position = extro.Coord(current_x, y, extro.CoordType.ABSOLUTE)
    time.start()


time = extro.Utils.Timeout(0)
time.on_finish.connect(next_frame)
time.start()


def increment_amplitude(increment: int):
    global amplitude
    amplitude += increment


def increment_frequency(increment: float):
    global frequency
    frequency += increment


extro.Services.InputService.on_event.connect(
    lambda _: increment_amplitude(10),
    extro.Services.InputService.SubscriberType.PRESS,
    extro.Services.InputService.Key.E,
)
extro.Services.InputService.on_event.connect(
    lambda _: increment_amplitude(-10),
    extro.Services.InputService.SubscriberType.PRESS,
    extro.Services.InputService.Key.Q,
)
extro.Services.InputService.on_event.connect(
    lambda _: increment_frequency(0.01),
    extro.Services.InputService.SubscriberType.PRESS,
    extro.Services.InputService.Key.W,
)
extro.Services.InputService.on_event.connect(
    lambda _: increment_frequency(-0.01),
    extro.Services.InputService.SubscriberType.PRESS,
    extro.Services.InputService.Key.S,
)

extro.Engine.start()
