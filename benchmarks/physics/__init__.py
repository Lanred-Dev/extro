import benchmarks.benchmarker as benchmarker
import extro

extro.Services.WorldService.set_tile_size(6)
extro.Window.set_title("Physics Benchmark")
extro.Window.set_size(extro.Vector2(700, 700))

NUMBER_OF_INSTANCES: int = 2500

benchmarker.start_tracking(
    "./benchmarks/physics",
    10,
    {
        "name": "Physics Benchmark",
        "Number of Instances": str(NUMBER_OF_INSTANCES),
    },
)

scene = extro.Instances.World.Scene()

for index in range(NUMBER_OF_INSTANCES):
    column_index = index // 2
    size: extro.Coord = extro.Coord(1, 1, extro.Coord.CoordType.WORLD)
    position: extro.Coord = extro.Coord(
        0, 0.4 if index % 2 == 0 else 0.5, extro.Coord.CoordType.NORMALIZED
    )
    position.absolute_x = size.absolute_x * (1.3 * column_index)

    rect = extro.Instances.World.Rectangle(
        position=position,
        size=size,
        color=extro.RGBAColor(255, 0, 0),
    )
    physics_body = extro.Instances.Core.Components.PhysicsBody(
        owner=rect.id,
        mass=1.0,
        body_type=extro.Services.PhysicsService.PhysicsBodyType.DYNAMIC,
    )
    rect.add_component(physics_body)
    collider = extro.Instances.Core.Components.Collider(
        owner=rect.id,
        is_collidable=True,
    )
    rect.add_component(collider)
    scene.add(rect)
    physics_body.add_force(
        extro.Vector2(10, 300 if index % 2 == 0 else -300),
        extro.Vector2(1, 0),
    )

extro.Engine.start()
