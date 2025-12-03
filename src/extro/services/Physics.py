"""Provides physics-related constants and types."""

from enum import auto, Enum
import extro.internal.systems.Physics.PhysicsSolver as PhysicsSolver

dampening: float = 0.8


class PhysicsBodyType(Enum):
    DYNAMIC = auto()
    STATIC = auto()
    KINEMATIC = auto()


def set_impulse_scaler(scaler: float):
    """Sets the impulse scaler used in collision resolution."""
    PhysicsSolver.set_impulse_scaler(scaler)


def set_dampening(value: float):
    """Sets the global dampening factor for physics bodies."""
    global dampening
    dampening = value


__all__ = [
    "PhysicsBodyType",
    "set_impulse_scaler",
    "set_dampening",
]
