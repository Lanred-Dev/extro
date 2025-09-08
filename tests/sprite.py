# python -m tests.sprite

import src as extro

scene = extro.Instances.Scene()

sprite = extro.Instances.world.Sprite(
    image="C:\\Users\\lando\\Documents\\Programming\\simple-game\\tests\\cats.png"
)
sprite.size = extro.Vector2(100, 100)
scene.add_instance(sprite)

extro.start()
