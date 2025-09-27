from extro.core.Instance.Drawable import DrawableInstance
import extro.Console as Console


class UIInstance(DrawableInstance):
    def add_physics_body(self, *_: object, **__: object):
        Console.log("`UIInstance` cannot have a physics body", Console.LogType.WARNING)

    def add_collider(self, *_: object, **__: object):
        Console.log("`UIInstance` cannot have a collider", Console.LogType.WARNING)
