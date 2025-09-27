# python -m examples.square

import extro as extro

extro.Services.RenderService.set_fps(60)
extro.Services.WorldService.set_tile_size(100)
extro.Window.set_title("Square Test")

scene = extro.Instances.Scene()
rect = extro.Instances.world.Rectangle(
    position=extro.Vector2(1, 1), size=extro.Vector2(2, 2), color=extro.Color(255, 0, 0)
)
scene.add(rect)

extro.Engine.start()
