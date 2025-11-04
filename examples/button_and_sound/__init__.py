"""
The audio in this example is from https://pixabay.com/sound-effects/coin-257878
"""

import extro

extro.Services.RenderService.set_fps(60)
extro.Window.set_title("Button = sound effect")

coin_sound = extro.Instances.Audio.EffectAudio(
    audio_file="examples/button_and_sound/sound.mp3",
    volume=0.5,
    pitch=1.0,
    behavior=extro.Services.AudioService.AudioSourceBehaviorType.NON_SPATIAL,
)

layer = extro.Instances.UI.Layer()
button = extro.Instances.UI.Button(
    color=extro.RGBAColor(0, 0, 255),
    size=extro.Coord(0.2, 0.1, extro.Coord.CoordType.NORMALIZED),
    position=extro.Coord(0.5, 0.5, extro.Coord.CoordType.NORMALIZED),
    anchor=extro.Vector2(0.5, 0.5),
)
button.on_click.connect(lambda: coin_sound.source.play())
layer.add(button)

text = extro.Instances.UI.Text(
    text="Click Me",
    font=extro.Assets.Fonts.Arial,
    font_size=20,
    character_spacing=2,
    color=extro.RGBAColor(255, 255, 255),
    position=extro.Coord(0.5, 0.5, extro.Coord.CoordType.RELATIVE),
    anchor=extro.Vector2(0.5, 0.5),
)
layer.add(text)
text.hierarchy.parent = button

extro.Engine.start()
