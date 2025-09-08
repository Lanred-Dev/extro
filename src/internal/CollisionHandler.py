from typing import TYPE_CHECKING, List, Tuple, Dict


from src.internal.Console import Console, LogType
from src.internal.InstanceHandler import InstanceHandler

if TYPE_CHECKING:
    from src.instances.core.CollisionInstance import CollisionInstance


def is_instance_collidable(instance_id: str) -> bool:
    return (
        getattr(InstanceHandler.instances[instance_id], "is_collidable", None) != None
    )


class CollisionHandlerCls:
    """
    Central renderer manager for handling scenes and rendering order.

    Keeps track of active render targets (scenes) and ensures they
    are rendered in the correct order based on z-index.
    """

    _instances: List[str]
    _collidable: Dict[str, List[str]]
    _collisions: List[Tuple[str, str]]

    def __init__(self):
        self._instances = []
        self._collidable = {}
        self._collisions = []

    def register_instance(self, instance_id: str):
        if not is_instance_collidable(instance_id):
            Console.log(
                f"{instance_id} cannot be registered as collidable because it is not",
                LogType.ERROR,
            )
            return

        self._instances.append(instance_id)
        Console.log(f"{instance_id} was registered as collidable")
        self.update_collidable_instances_list()

    def unregister_instance(self, instance_id: str):
        if instance_id not in self._instances:
            Console.log(
                f"{instance_id} does not exist as a collidable instance", LogType.ERROR
            )
            return

        self._instances.remove(instance_id)
        Console.log(f"{instance_id} was unregistered as collidable")
        self.update_collidable_instances_list()

    def update_collisions(self):
        collisions: List[Tuple[str, str]] = []

        for collision_group, instances in self._collidable.items():
            for index, instance1_id in enumerate(instances):
                for instance2_id in instances[index + 1 :]:
                    instance1: "CollisionInstance" = InstanceHandler.instances[instance1_id]  # type: ignore
                    instance2: "CollisionInstance" = InstanceHandler.instances[instance2_id]  # type: ignore

                    if instance1._collision_mask.collides_with(
                        instance2._collision_mask
                    ):
                        collisions.append((instance1_id, instance2_id))

        # Handle collision end
        for collision in self._collisions:
            if collision not in collisions:
                instance1: "CollisionInstance" = InstanceHandler.instances[collision[0]].on_collision_end.fire()  # type: ignore
                instance2: "CollisionInstance" = InstanceHandler.instances[collision[1]].on_collision_end.fire()  # type: ignore

        # Handle collision start
        for collision in collisions:
            if collision not in self._collisions:
                instance1: "CollisionInstance" = InstanceHandler.instances[collision[0]].on_collision.fire()  # type: ignore
                instance2: "CollisionInstance" = InstanceHandler.instances[collision[1]].on_collision.fire()  # type: ignore

        self._collisions = collisions

    def update_collidable_instances_list(self):
        self._collidable.clear()

        for instance_id in self._instances:
            if not is_instance_collidable(instance_id):
                continue

            collision_group: str = InstanceHandler.instances[instance_id]._collision_group  # type: ignore

            if collision_group not in self._collidable:
                self._collidable[collision_group] = []

            self._collidable[collision_group].append(instance_id)

        Console.log(
            f"CollisionHandler is handling {sum(len(ids) for ids in self._collidable.values())} instances"
        )


CollisionHandler = CollisionHandlerCls()
__all__ = ["CollisionHandler"]
