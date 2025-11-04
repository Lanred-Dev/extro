import extro

extro.Services.RenderService.set_fps(144)
extro.Services.WorldService.set_tile_size(25)
extro.Window.set_title("They bounce off each other!")

scene = extro.Instances.World.Scene()

rect1 = extro.Instances.World.Rectangle(
    position=extro.Coord(100, 100, extro.Coord.CoordType.ABSOLUTE),
    size=extro.Coord(2, 2, extro.Coord.CoordType.WORLD),
    color=extro.RGBAColor(255, 0, 0),
)
physics_body1 = extro.Instances.Core.Components.PhysicsBody(
    owner=rect1.id,
    mass=1.0,
    is_anchored=False,
)
rect1.add_component(physics_body1)
collider1 = extro.Instances.Core.Components.Collider(
    owner=rect1.id,
    is_collidable=True,
)
rect1.add_component(collider1)
scene.add(rect1)
physics_body1.apply_force(extro.Vector2(100, 100), extro.Vector2(1, 0))

rect2 = extro.Instances.World.Rectangle(
    position=extro.Coord(300, 300, extro.Coord.CoordType.ABSOLUTE),
    size=extro.Coord(100, 100, extro.Coord.CoordType.ABSOLUTE),
    color=extro.RGBAColor(0, 255, 0),
)
physics_body2 = extro.Instances.Core.Components.PhysicsBody(
    owner=rect2.id,
    mass=1.0,
    is_anchored=False,
)
rect2.add_component(physics_body2)
collider2 = extro.Instances.Core.Components.Collider(
    owner=rect2.id,
    is_collidable=True,
)
rect2.add_component(collider2)
scene.add(rect2)
physics_body2.apply_force(extro.Vector2(-200, -200))

extro.Engine.start()
