# python -m tests.text

import src as extro

extro.Renderer.set_fps(60)
extro.Window.set_title("Text Test")

scene = extro.Instances.Scene(type=extro.Renderer.RenderTargetType.INDEPENDENT)
text = extro.Instances.ui.Text(
    "Hello, World!", extro.Instances.ui.Fonts.Arial, 20, character_spacing=2
)
text.position = extro.Vector2(0.1, 0.1)
text.color = extro.Color(255, 0, 0)
scene.add(text)

extro.Engine.start()
