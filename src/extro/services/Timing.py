"""Provides timing-related events and delta time."""

from extro.utils.Signal import Signal

delta: float = 0
on_pre_render: Signal = Signal()
on_post_render: Signal = Signal()
on_pre_physics: Signal = Signal()

__all__ = ["delta", "on_pre_render", "on_post_render", "on_pre_physics"]
