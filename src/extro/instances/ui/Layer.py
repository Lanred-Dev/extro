from extro.instances.core.RenderTarget import RenderTarget
import extro.services.Render as RenderService


class Layer(RenderTarget):
    def __init__(self, zindex: int = 0, is_visible: bool = True):
        super().__init__(RenderService.RenderTargetType.INDEPENDENT, zindex, is_visible)
