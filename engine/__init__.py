import pygame

pygame.init()

import sys
import typing
from .components import Signal
from .utils.id import generate_id
from .Console import console, LogType


def is_instance_collidable(instance: typing.Any) -> bool:
    if hasattr(instance, "is_collidable") and instance.is_collidable:
        if not hasattr(instance, "collision_mask") or not isinstance(
            instance.collision_mask, pygame.Mask
        ):
            console.log(
                f"Instance {instance.id} was marked as `is_collidable` but did not have a valid `collision_mask`.",
                LogType.ERROR,
            )
            return False
        elif not hasattr(instance, "collision_group") or not isinstance(
            instance.collision_group, str
        ):
            console.log(
                f"Iinstance {instance.id} was marked as `is_collidable` but did not have a valid `collision_group`.",
                LogType.ERROR,
            )
            return False

        return True

    return False


class Engine:
    """Core engine class that manages the game loop, events, and instances."""

    delta: float = 0
    fps: int = 144
    screen: pygame.Surface = pygame.display.set_mode((500, 500))
    clock: pygame.time.Clock = pygame.time.Clock()
    instances: dict[str, typing.Any] = {}
    collision_groups: dict[str, list[str]] = {}

    on_input: Signal = Signal()
    on_click: Signal = Signal()
    on_tick: Signal = Signal()

    __is_running: bool = True
    __render_list: list[str] = []
    __collidable_instances: list[str] = []

    def __init__(self):
        self.on_input.connect(console.handle_input)

    def start(self):
        """Start the engine's main loop."""
        console.log("Engine started")

        while self.__is_running:
            self.__tick()

        self.quit()

    def create_instance_id(self) -> str:
        return generate_id(10, "i_")

    def register_instance(self, id: str, instance: typing.Any) -> str:
        """
        Register an instance with the engine and generate a unique ID for it.

        The instance will be added to the engine's registry and updated every tick
        if it has a `tick()` method.

        Returns
        -------
        str
            The automatically generated unique ID assigned to the instance.
        """
        self.instances[id] = instance
        console.log(f"Instance registered with ID {id}")

        self.update_instance_render_list()
        self.update_collidable_instances_list()

        return id

    def unregister_instance(self, id: str):
        """Unregister an instance from the engine."""
        if id not in self.instances:
            console.log(f"Instance with ID {id} does not exist.", LogType.WARNING)
            return

        self.instances.pop(id, None)
        console.log(f"Instance with ID {id} was unregistered")

        self.update_instance_render_list()
        self.update_collidable_instances_list()

    def quit(self):
        """Stops the engine, quits Pygame, and exits the program."""
        pygame.quit()
        sys.exit()

    def __tick(self):
        """Perform a single engine tick."""

        self.screen.fill((0, 0, 0))
        self.__update_collision_groups()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__is_running = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.on_click.fire(event)
            elif event.type == pygame.KEYDOWN:
                self.on_input.fire(event)

        self.on_tick.fire()

        # Update all instances
        for id in self.__render_list:
            instance = self.instances[id]

            if hasattr(instance, "predraw"):
                instance.predraw()

        for id in self.__render_list:
            instance = self.instances[id]

            if hasattr(instance, "draw"):
                instance.draw()

        for id in self.__render_list:
            instance = self.instances[id]

            if hasattr(instance, "afterdraw"):
                instance.afterdraw()

        # Render the console on top of everything
        console.tick(
            self.screen, str(round(1.0 / self.delta if self.delta > 0 else 0, 2))
        )

        pygame.display.flip()
        self.delta = self.clock.tick(self.fps) / 1000

    def update_instance_render_list(self):
        self.__render_list = [
            instance.id
            for instance in sorted(
                self.instances.values(), key=lambda instance: instance.zindex
            )
        ]

        console.log(f"{len(self.__render_list)} instances")

    def update_collidable_instances_list(self):
        self.__collidable_instances = [
            id
            for id, instance in self.instances.items()
            if is_instance_collidable(instance)
        ]

        console.log(f"{len(self.__collidable_instances)} collidable instances")

    def __update_collision_groups(self):
        self.collision_groups = {}

        for id in self.__collidable_instances.copy():
            instance = self.instances[id]

            if instance.collision_group not in self.collision_groups:
                self.collision_groups[instance.collision_group] = []

            self.collision_groups[instance.collision_group].append(id)


engine = Engine()
