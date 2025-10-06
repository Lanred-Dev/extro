from extro.instances.core.RenderTarget import RenderTarget
import extro.internal.systems.Render as RenderSystem


class Scene(RenderTarget):
    def __init__(self, zindex: int = 0, is_visible: bool = True):
        super().__init__(RenderSystem.RenderTargetType.WORLD, zindex, is_visible)
