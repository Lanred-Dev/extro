# python -m tests.animated_sprite

import src as extro

extro.Renderer.set_fps(60)
extro.Window.set_title("Animated Sprite Test")

scene = extro.Instances.Scene()
sprite = extro.Instances.world.Sprite(
    image_path="tests/animated_sprite/sprite.png",
    is_animated=True,
    frame_size=extro.Vector2(18, 14),
    frame_time=0.1,
    starting_frame=0,
)
sprite.size = extro.Vector2(3, 3)
scene.add(sprite)

extro.Engine.start()
