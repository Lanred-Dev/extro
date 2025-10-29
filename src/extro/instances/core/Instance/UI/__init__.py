from extro.instances.core.Instance.Renderable import Renderable
import extro.internal.systems.UI as UISystem


class UIInstance(Renderable):
    __slots__ = Renderable.__slots__ + ("_type",)

    _type: "UISystem.UIInstanceType"

    def __init__(self, type: "UISystem.UIInstanceType", **kwargs):
        super().__init__(**kwargs)

        self._type = type
        UISystem.instances.register(self._id)
        self._janitor.add(UISystem.instances.unregister, self._id)
