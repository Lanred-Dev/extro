import benchmarks.benchmarker as benchmarker
import extro

extro.Services.WorldService.set_tile_size(6)
extro.Window.set_title("Instance Benchmark")
extro.Window.set_size(extro.Vector2(700, 700))

TARGET_NUMBER_OF_INSTANCES: int = 50000

benchmarker.start_tracking()

scene = extro.Instances.World.Scene()
instances_created: int = 0
pre_render_connection: str


def create_instance():
    global instances_created

    instances_created += 1
    x, y = extro.Services.ScreenService.random_absolute_coords()
    rect = extro.Instances.World.Rectangle(
        position=extro.Coord(x, y, extro.Coord.CoordType.ABSOLUTE),
        size=extro.Coord(1, 1, extro.Coord.CoordType.WORLD),
        color=extro.RGBAColor(255, 0, 0),
    )
    scene.add(rect)

    if instances_created >= TARGET_NUMBER_OF_INSTANCES:
        extro.Services.TimingService.on_pre_render.disconnect(pre_render_connection)
        benchmarker.stop_tracking(
            "./benchmarks/instances",
            {
                "name": "Instance Benchmark",
                "Number of Instances": str(instances_created),
            },
        )


def on_frame():
    for _ in range(50):
        create_instance()


pre_render_connection = extro.Services.TimingService.on_pre_render.connect(on_frame)

extro.Engine.start()
