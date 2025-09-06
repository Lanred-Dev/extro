# python -m tests.square

import src

scene1 = src.Instances.Scene("testing_scene")


rec1 = src.Instances.world.Rectangle()
rec1.set_color(src.Color(255, 0, 0))
rec1.set_size(src.Vector2(800, 600))
scene1.add_instance(rec1)

src.start()
