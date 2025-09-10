# python -m tests.sprite

import src as extro

extro.Renderer.set_fps(60)
extro.Window.title = "Sprite Test"

scene = extro.Instances.Scene()
sprite = extro.Instances.world.Sprite(
    image_path="C:\\Users\\lando\\Documents\\Programming\\simple-game\\tests\\sprite\\sprite.png"
)
sprite.size = extro.Vector2(3, 3)
scene.add_instance(sprite)

extro.Engine.start()
