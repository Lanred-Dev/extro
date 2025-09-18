from src.animation.easings.linear import linear
from src.internal.shared_types import EasingFunction

easings: dict[str, EasingFunction] = {"linear": linear}

__all__ = ["easings"]
