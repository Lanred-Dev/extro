# python -m examples.text

import extro as extro

extro.services.RenderService.set_fps(60)
extro.Window.set_title("Text Test")

scene = extro.Instances.Scene(
    type=extro.services.RenderService.RenderTargetType.INDEPENDENT
)
text = extro.Instances.ui.Text(
    text="Hello, World!",
    font=extro.Instances.ui.Fonts.Arial,
    font_size=20,
    character_spacing=2,
    color=extro.Color(255, 255, 255),
    position=extro.Coord(0, 0, extro.CoordType.NORMALIZED),
)
scene.add(text)

extro.Engine.start()
