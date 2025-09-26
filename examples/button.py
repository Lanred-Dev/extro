# python -m examples.button

import extro as extro

extro.services.RenderService.set_fps(60)
extro.Window.set_title("Button Test")

scene = extro.Instances.Scene(
    type=extro.services.RenderService.RenderTargetType.INDEPENDENT
)
button = extro.Instances.ui.Button(
    color=extro.Color(0, 0, 255),
    size=extro.Vector2(0.2, 0.1),
    position=extro.Vector2(0.5, 0.5),
)
button.on_click.connect(lambda: print("Button clicked!"))
scene.add(button)

text = extro.Instances.ui.Text(
    text="Click Me",
    font=extro.Instances.ui.Fonts.Arial,
    font_size=20,
    character_spacing=2,
    color=extro.Color(255, 255, 255),
    position=extro.Vector2(0.5, 0.5),
    anchor=extro.Vector2(0.5, 0.5),
    is_position_relative=True,
)
button.add_child(text)

extro.Engine.start()
