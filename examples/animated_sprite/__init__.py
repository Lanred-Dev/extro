"""
The sprite in this examples is from https://opengameart.org/content/cat-fighter-sprite-sheet
"""

import extro

extro.Services.RenderService.set_fps(60)
extro.Window.set_title("Animated Sprite")

scene = extro.Instances.world.Scene()
sprite = extro.Instances.world.AnimatedSprite(
    image_file="examples/animated_sprite/sprite.png",
    frame_size=extro.Vector2(64, 64),
    frame_duration=0.125,
    size=extro.Coord(5, 5, extro.Coord.CoordType.WORLD),
    position=extro.Coord(0.5, 0.5, extro.Coord.CoordType.NORMALIZED),
    anchor=extro.Vector2(0.5, 0.5),
    frame_count=13,
)
scene.add(sprite)

extro.Engine.start()
