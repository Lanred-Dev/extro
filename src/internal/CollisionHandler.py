from typing import TYPE_CHECKING, List, Tuple


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

    __instances: List[str]
    __collidable: List[str]

    def __init__(self):
        self.__instances = []
        self.__collidable = []
        self.__collisions = []

    def register_instance(self, instance: str):
        if not is_instance_collidable(instance):
            Console.log(
                f"{instance} cannot be registered as collidable because it is not",
                LogType.ERROR,
            )
            return

        self.__instances.append(instance)
        Console.log(f"{instance} was registered as collidable")
        self.update_collidable_instances_list()

    def unregister_instance(self, instance: str):
        if instance not in self.__instances:
            Console.log(
                f"{instance} does not exist as a collidable instance", LogType.ERROR
            )
            return

        self.__instances.remove(instance)
        Console.log(f"{instance} was unregistered as collidable")
        self.update_collidable_instances_list()

    def update_collisions(self):
        collisions: List[Tuple[str, str]] = []

        for index, instance1_id in enumerate(self.__collidable):
            for instance2_id in self.__collidable[index + 1 :]:
                instance1: CollisionInstance = InstanceHandler.instances[instance1_id]  # type: ignore
                instance2: CollisionInstance = InstanceHandler.instances[instance2_id]  # type: ignore

                if instance1.collision_group != instance2.collision_group:
                    continue

                if instance1.collision_mask.collides_with(instance2.collision_mask):
                    collisions.append((instance1_id, instance2_id))

        # Handle collision end
        for collision in self.__collisions:
            if collision not in collisions:
                instance1: CollisionInstance = InstanceHandler.instances[collision[0]]  # type: ignore
                instance1.on_collision_end.fire()
                instance2: CollisionInstance = InstanceHandler.instances[collision[1]]  # type: ignore
                instance2.on_collision_end.fire()

        # Handle collision start
        for collision in collisions:
            if collision not in self.__collisions:
                instance1: CollisionInstance = InstanceHandler.instances[collision[0]]  # type: ignore
                instance1.on_collision.fire()
                instance2: CollisionInstance = InstanceHandler.instances[collision[1]]  # type: ignore
                instance2.on_collision.fire()

        self.__collisions = collisions

    def update_collidable_instances_list(self):
        self.__collidable = [
            instance_id
            for instance_id in self.__instances
            if is_instance_collidable(instance_id)
        ]

        Console.log(f"CollisionHandler is handling {len(self.__collidable)} instances")


CollisionHandler = CollisionHandlerCls()
__all__ = ["CollisionHandler"]
