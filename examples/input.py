import extro

extro.Services.RenderService.set_fps(60)
extro.Window.set_title("Text Input")

layer = extro.Instances.ui.Layer()

input = extro.Instances.ui.TextInput(
    font_size=20,
    size=extro.Coord(0.4, 0.1, extro.Coord.CoordType.NORMALIZED),
    position=extro.Coord(0.5, 0.5, extro.Coord.CoordType.NORMALIZED),
    anchor=extro.Vector2(0.5, 0.5),
    color=extro.RGBAColor(0, 0, 255),
)
layer.add(input)

extro.Engine.start()
