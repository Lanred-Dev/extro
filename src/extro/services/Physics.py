from extro.utils.Signal import Signal

dampening: float = 0.8

on_pre_physics = Signal()

__all__ = [
    "dampening",
    "on_pre_physics",
]
