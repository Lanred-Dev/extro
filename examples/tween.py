import extro

extro.Services.RenderService.set_fps(60)
extro.Services.WorldService.set_tile_size(50)
extro.Window.set_title("Tweening... its so smooth")

scene = extro.Instances.World.Scene()

rect = extro.Instances.World.Rectangle(
    position=extro.Coord(
        0,
        0,
        extro.Coord.CoordType.ABSOLUTE,
    ),
    size=extro.Coord(2, 2, extro.Coord.CoordType.WORLD),
    color=extro.RGBAColor(255, 0, 0),
)
scene.add(rect)

tween = extro.Animation.Tween(
    start=extro.Vector2(0, 0),
    end=extro.Vector2(extro.Window.size.x, extro.Window.size.y),
    duration=6.0,
)


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def on_update():
    rect.transform.position = extro.Coord(
        clamp(tween.value.x, 0, extro.Window.size.x - rect.transform.size.absolute_x),
        clamp(tween.value.y, 0, extro.Window.size.y - rect.transform.size.absolute_y),
        extro.Coord.CoordType.ABSOLUTE,
    )


tween.on_update.connect(on_update)
tween.play()

extro.Engine.start()
