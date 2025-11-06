import benchmarks.benchmarker as benchmarker
import extro

extro.Services.WorldService.set_tile_size(6)
extro.Window.set_title("Animation Benchmark")
extro.Window.set_size(extro.Vector2(700, 700))

NUMBER_OF_INSTANCES: int = 5000

benchmarker.start_tracking(
    "./benchmarks/animation",
    6,
    {
        "name": "Animation Benchmark",
        "Number of Instances": str(NUMBER_OF_INSTANCES),
    },
)

scene = extro.Instances.World.Scene()


def update_tween_position(value: extro.Vector2, rect):
    rect.transform.position = extro.Coord(
        value.x,
        value.y,
        extro.Coord.CoordType.ABSOLUTE,
    )


for index in range(NUMBER_OF_INSTANCES):
    x, y = extro.Services.ScreenService.random_absolute_coords()
    dx, dy = extro.Services.ScreenService.random_absolute_coords()
    rect = extro.Instances.World.Rectangle(
        position=extro.Coord(x, y, extro.Coord.CoordType.ABSOLUTE),
        size=extro.Coord(1, 1, extro.Coord.CoordType.WORLD),
        color=extro.RGBAColor(255, 0, 0),
    )
    scene.add(rect)

    tween = extro.Animation.Tween(
        start=extro.Vector2(x, y),
        end=extro.Vector2(dx, dy),
        duration=5.0,
    )
    tween.on_update.connect(lambda value, r=rect: update_tween_position(value, r))
    tween.play()

extro.Engine.start()
