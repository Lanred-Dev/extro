import extro

extro.Services.RenderService.set_fps(60)
extro.Window.set_title("Animated Sprite")

scene = extro.Instances.world.Scene()
sprite = extro.Instances.world.AnimatedSprite(
    image_file="examples/animated_sprite/sprite.png",
    frame_size=extro.Vector2(18, 14),
    frame_duration=0.1,
    size=extro.Coord(3, 3 * (14 / 18), extro.CoordType.WORLD),
    position=extro.Coord(0, 0, extro.CoordType.WORLD),
    frame_count=14,
)
scene.add(sprite)

extro.Engine.start()
