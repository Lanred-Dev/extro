import math
import extro

extro.Services.RenderService.set_fps(60)
extro.Window.set_title("Animated sin wave")

scene = extro.Instances.world.Scene()

rect = extro.Instances.world.Rectangle(
    position=extro.Coord(0, 0, extro.Coord.CoordType.ABSOLUTE),
    size=extro.Coord(15, 15, extro.Coord.CoordType.ABSOLUTE),
    color=extro.RGBAColor(255, 0, 0),
)
scene.add(rect)

amplitude: int = 100
frequency: float = 0.1
current_x = 0


def next_frame():
    global current_x

    if current_x >= extro.Window.size.x:
        current_x = 0
    else:
        current_x += 60 * extro.Services.TimingService.delta

    y: float = math.sin(current_x * frequency) * amplitude + (extro.Window.size.y / 2)
    rect.transform.position = extro.Coord(current_x, y, extro.Coord.CoordType.ABSOLUTE)


extro.Services.TimingService.on_pre_render.connect(next_frame)


def increment_amplitude(increment: int):
    global amplitude
    amplitude += increment
    extro.Console.log(f"Amplitude: {amplitude}")


def increment_frequency(increment: float):
    global frequency
    frequency += increment
    extro.Console.log(f"Frequency: {frequency}")


extro.Services.InputService.on_event.connect(
    lambda _: increment_amplitude(10),
    extro.Services.InputService.SubscriberType.PRESS,
    extro.Services.InputService.Keyboard.E,
)
extro.Services.InputService.on_event.connect(
    lambda _: increment_amplitude(-10),
    extro.Services.InputService.SubscriberType.PRESS,
    extro.Services.InputService.Keyboard.Q,
)
extro.Services.InputService.on_event.connect(
    lambda _: increment_frequency(0.01),
    extro.Services.InputService.SubscriberType.PRESS,
    extro.Services.InputService.Keyboard.W,
)
extro.Services.InputService.on_event.connect(
    lambda _: increment_frequency(-0.01),
    extro.Services.InputService.SubscriberType.PRESS,
    extro.Services.InputService.Keyboard.S,
)

extro.Engine.start()
