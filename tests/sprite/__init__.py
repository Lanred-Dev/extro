# python -m tests.sprite

import src as extro

extro.Renderer.set_fps(60)
extro.Window.set_title("Sprite Test")

scene = extro.Instances.Scene()
sprite = extro.Instances.world.Sprite(
    image_path="tests/sprite/sprite.png",
)
sprite.size = extro.Vector2(3, 3)
scene.add(sprite)

extro.Engine.start()
