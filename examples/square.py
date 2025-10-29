import extro

extro.Services.RenderService.set_fps(60)
extro.Services.WorldService.set_tile_size(50)
extro.Window.set_title("Square.")

scene = extro.Instances.world.Scene()


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


position_x, position_y = extro.Services.ScreenService.random_absolute_coords()
size = extro.Coord(2, 2, extro.Coord.CoordType.WORLD)
rect = extro.Instances.world.Rectangle(
    position=extro.Coord(
        clamp(
            position_x,
            0,
            extro.Window.size.x - size.absolute_x,
        ),
        clamp(
            position_y,
            0,
            extro.Window.size.y - size.absolute_y,
        ),
        extro.Coord.CoordType.ABSOLUTE,
    ),
    size=size,
    color=extro.RGBAColor(255, 0, 0),
)
scene.add(rect)

extro.Engine.start()
