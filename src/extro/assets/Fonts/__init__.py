from importlib import resources

from extro.instances.ui.Font import Font

Arial: Font = Font(str(resources.files("extro.assets.Fonts") / "arial.ttf"))

__all__ = ["Arial"]
