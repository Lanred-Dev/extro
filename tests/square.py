# python -m tests.square

import src as extro

scene = extro.Instances.Scene()

rec = extro.Instances.world.Rectangle()
rec.color = extro.Color(255, 0, 0)
rec.size = extro.Vector2(500, 500)
rec.position = extro.Vector2(500, 500)
rec.anchor = extro.Vector2(1, 1)
scene.add_instance(rec)

extro.start()
