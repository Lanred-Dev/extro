# python -m examples.physics

import extro as extro

extro.Services.RenderService.set_fps(1000)
extro.Services.WorldService.set_tile_size(20)
extro.Window.set_title("Physics Test")

scene = extro.Instances.Scene()

rect1 = extro.Instances.world.Rectangle(
    position=extro.Coord(1, 1, extro.CoordType.WORLD), size=extro.Coord(2, 2, extro.CoordType.WORLD), color=extro.Color(255, 0, 0)
)
rect1.add_collider()
rect1.add_physics_body(1)
rect1.physics_body.apply_force(extro.Vector2(18, 5))
scene.add(rect1)

rect2 = extro.Instances.world.Rectangle(
    position=extro.Coord(5, 5, extro.CoordType.WORLD), size=extro.Coord(2, 2, extro.CoordType.WORLD), color=extro.Color(255, 0, 0)
)
rect2.add_collider()
rect2.add_physics_body(1)
rect2.physics_body.apply_force(extro.Vector2(-500, -500))
scene.add(rect2)

extro.Engine.start()
