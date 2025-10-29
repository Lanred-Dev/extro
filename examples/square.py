import extro

extro.Services.RenderService.set_fps(60)
extro.Services.WorldService.set_tile_size(50)
extro.Window.set_title("Square.")

scene = extro.Instances.world.Scene()
rect = extro.Instances.world.Rectangle(
    position=extro.Coord(0.5, 0.5, extro.Coord.CoordType.NORMALIZED),
    size=extro.Coord(2, 2, extro.Coord.CoordType.WORLD),
    color=extro.RGBAColor(255, 0, 0),
    anchor=extro.Vector2(0.5, 0.5),
)
scene.add(rect)

extro.Engine.start()
