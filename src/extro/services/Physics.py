from enum import auto, Enum

dampening: float = 0.8


class PhysicsBodyType(Enum):
    DYNAMIC = auto()
    STATIC = auto()
    KINEMATIC = auto()


__all__ = [
    "dampening",
    "PhysicsBodyType",
]
