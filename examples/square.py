import extro

extro.Services.RenderService.set_fps(60)
extro.Services.WorldService.set_tile_size(100)
extro.Window.set_title("Square.")

scene = extro.Instances.world.Scene()

position_x, position_y = extro.Services.ScreenService.random_absolute_coords()
rect = extro.Instances.world.Rectangle(
    position=extro.Coord(position_x, position_y, extro.CoordType.ABSOLUTE),
    size=extro.Coord(2, 2, extro.CoordType.WORLD),
    color=extro.RGBAColor(255, 0, 0),
)
scene.add(rect)

extro.Engine.start()
