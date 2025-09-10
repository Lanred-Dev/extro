# python -m tests.square

import src as extro

extro.Renderer.set_fps(60)
extro.Renderer.set_world_tile_size(100)
extro.Window.title = "Square Test"

scene = extro.Instances.Scene()
rect = extro.Instances.world.Rectangle(
    position=extro.Vector2(1, 1), size=extro.Vector2(2, 2), color=extro.Color(255, 0, 0)
)
scene.add_instance(rect)

extro.Engine.start()
