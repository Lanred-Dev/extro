from extro.animation.easings.linear import linear
from extro.internal.shared_types import EasingFunction

easings: dict[str, EasingFunction] = {"linear": linear}

__all__ = ["easings"]
