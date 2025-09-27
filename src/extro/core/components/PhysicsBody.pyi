from extro.shared.Vector2 import Vector2

class PhysicsBody:
    mass: float
    desired_velocity: Vector2

    def __init__(
        self,
        owner_id: int,
        mass: float,
        restitution: float = 0.2,
        is_anchored: bool = False,
    ): ...
    def destroy(self): ...
    def apply_force(self, force: Vector2): ...
    @property
    def is_anchored(self) -> bool: ...
    @is_anchored.setter
    def is_anchored(self, is_anchored: bool): ...
