from extro.instances.world.Sprite.Animated import AnimatedSprite
import extro.services.Input as InputService
import extro.services.Physics as PhysicsService
from extro.shared.Vector2 import Vector2
import extro.Console as Console


class PlayableCharacter(AnimatedSprite):
    _speed: float
    _last_movement_state: str
    _forced_state: str | None
    _actual_state: str
    _states: dict[str, Vector2]
    _direction_vector: Vector2

    def __init__(
        self,
        speed: float,
        image_file: str,
        frame_size: Vector2,
        states: dict[str, Vector2],
        mass=0.1,
        **kwargs,
    ):
        super().__init__(image_file=image_file, frame_size=frame_size, **kwargs)

        self._speed = speed
        self._states = {}
        self._last_movement_state = "move.down"
        self._direction_vector = Vector2(0, 0)
        self._forced_state = None
        self._actual_state = ""

        for name, position in states.items():
            self.add_state(name, position)

        self._set_state("idle.down")
        self.add_physics_body(mass, 0)
        self.add_collider()

        self._janitor.add(
            InputService.on_key_event.disconnect,
            InputService.on_key_event.connect(
                self._on_key_down, InputService.SubscriberType.PRESS
            ),
        )
        self._janitor.add(
            InputService.on_key_event.disconnect,
            InputService.on_key_event.connect(
                self._on_key_up, InputService.SubscriberType.RELEASE
            ),
        )
        self._janitor.add(
            PhysicsService.on_pre_physics.disconnect,
            PhysicsService.on_pre_physics.connect(self._update),
        )

    def add_state(self, state: str, frames: Vector2):
        self._states[state] = frames

    def set_state(self, state: str):
        if state not in self._states:
            Console.log(
                f"{self._id} does not have state '{state}'", Console.LogType.WARNING
            )
            return

        self._forced_state = state
        self._set_state(state)

    def _set_state(self, state: str):
        if self._actual_state == state or state not in self._states:
            return

        if state.startswith("move."):
            self._last_movement_state = state

        self._actual_state = state
        self._current_frame.x = 0
        # x = row, y = amount of columns
        self._current_frame.y = self._states[state].x
        self._frame_count = int(self._states[state].y)
        # Force frame update
        self._last_frame_at -= self._frame_duration

    def _on_key_down(self, key: InputService.Key):
        if key == InputService.get_action("move.left"):
            self._direction_vector.x = -1
        elif key == InputService.get_action("move.right"):
            self._direction_vector.x = 1
        elif key == InputService.get_action("move.up"):
            self._direction_vector.y = -1
        elif key == InputService.get_action("move.down"):
            self._direction_vector.y = 1

    def _on_key_up(self, key: InputService.Key):
        if not InputService.is_input_active(
            InputService.Key.A
        ) and not InputService.is_input_active(InputService.Key.D):
            self._direction_vector.x = 0

        if not InputService.is_input_active(
            InputService.Key.W
        ) and not InputService.is_input_active(InputService.Key.S):
            self._direction_vector.y = 0

    def _update(self):
        self.physics_body.desired_velocity.x = self._direction_vector.x * self._speed
        self.physics_body.desired_velocity.y = self._direction_vector.y * self._speed

        if self._forced_state:
            self._set_state(self._forced_state)
        elif self._direction_vector.x < 0:
            self._set_state("move.left")
        elif self._direction_vector.x > 0:
            self._set_state("move.right")
        elif self._direction_vector.y < 0:
            self._set_state("move.up")
        elif self._direction_vector.y > 0:
            self._set_state("move.down")
        else:
            movement_based_idle_state: str = f"idle.{self._last_movement_state}"

            if movement_based_idle_state in self._states:
                self._set_state(movement_based_idle_state)
            else:
                self._set_state("idle.down")

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = speed
