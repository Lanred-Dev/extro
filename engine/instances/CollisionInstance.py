from .AdvancedInstance import AdvancedInstance
from engine.components import Signal
from engine import engine
import pygame
from engine.Console import console


class CollisionInstance(AdvancedInstance):
    def __init__(self):
        super().__init__()
        # is_collidable will be set to true after init, where the first collision mask is created
        self.is_collidable: bool = False
        self.collision_group: str = ""
        self.colliding_with: list[str] = []
        self.collision_mask: pygame.Mask = pygame.mask.Mask((0, 0))
        self.on_collision: Signal = Signal()
        self.on_collision_end: Signal = Signal()

    def init(self):
        """Initialize the instance and set it as collidable."""
        super().init()
        self.set_collidable(True)

    def set_collidable(self, is_collidable: bool):
        """Enable or disable collision for this instance."""
        self.update_collision_mask()
        self.is_collidable: bool = is_collidable
        engine.update_collidable_instances_list()

    def afterdraw(self):
        new_colliding_with: list[str] = []

        # Determine what the instance is currently colliding with
        for group, instances in list(engine.collision_groups.items()):
            if group != self.collision_group:
                continue

            for id in instances:
                # Skip checking itself
                if self.id == id:
                    continue

                instance: CollisionInstance = engine.instances[id]
                offset: tuple[int, int] = (
                    int(instance.actual_position.x - self.actual_position.x),
                    int(instance.actual_position.y - self.actual_position.y),
                )

                if self.collision_mask.overlap(instance.collision_mask, offset):
                    new_colliding_with.append(id)

        # Determine what the instance is no longer colliding with
        for id in self.colliding_with:
            if id not in new_colliding_with:
                self.on_collision_end.fire(id)

        # Determine what the instance just started colliding with
        for id in new_colliding_with:
            if id not in self.colliding_with:
                self.on_collision.fire(id)

        self.colliding_with = new_colliding_with

    def update_collision_mask(self):
        """Rebuild the collision mask from the surface."""
        self.collision_mask = pygame.mask.from_surface(self.surface)
        console.log(f"Updating `collision_mask` for instance {self.id}")
