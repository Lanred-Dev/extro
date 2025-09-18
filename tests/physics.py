# python -m tests.physics

import src as extro

extro.Renderer.set_fps(1000)
extro.WorldService.set_world_tile_size(20)
extro.Window.set_title("Physics Test")

scene = extro.Instances.Scene()

rect1 = extro.Instances.world.Rectangle(
    position=extro.Vector2(1, 1), size=extro.Vector2(2, 2), color=extro.Color(255, 0, 0)
)
rect1.add_collider()
rect1.add_physics_body(1)
rect1.physics_body.apply_force(extro.Vector2(18, 5))
scene.add(rect1)

rect2 = extro.Instances.world.Rectangle(
    position=extro.Vector2(5, 5), size=extro.Vector2(2, 2), color=extro.Color(255, 0, 0)
)
rect2.add_collider()
rect2.add_physics_body(1)
rect2.physics_body.apply_force(extro.Vector2(-30, -25))
scene.add(rect2)

extro.Engine.start()
