import extro

extro.Services.RenderService.set_fps(60)
extro.Window.set_title("Click the button :)")

layer = extro.Instances.ui.Layer()
button = extro.Instances.ui.Button(
    color=extro.RGBAColor(0, 0, 255),
    size=extro.Coord(0.2, 0.1, extro.CoordType.NORMALIZED),
    position=extro.Coord(0.5, 0.5, extro.CoordType.NORMALIZED),
)
button.on_click.connect(lambda: print("Button clicked!"))
layer.add(button)

text = extro.Instances.ui.Text(
    text="Click Me",
    font=extro.Assets.Fonts.Arial,
    font_size=20,
    character_spacing=2,
    color=extro.RGBAColor(255, 255, 255),
    position=extro.Coord(0.5, 0.5, extro.CoordType.NORMALIZED),
    anchor=extro.Vector2(0.5, 0.5),
    scale_size_to_font=True,
)
layer.add(text)

extro.Engine.start()
