from extro.instances.world.Sprite.Animated import AnimatedSprite
import extro.services.Input as InputService
from extro.shared.Vector2 import Vector2


class PlayableCharacter(AnimatedSprite):
    _speed: float

    def __init__(self, speed: float, image_file: str, frame_size: Vector2, **kwargs):
        super().__init__(image_file=image_file, frame_size=frame_size, **kwargs)

        self._speed = speed

        self.add_physics_body(mass=0.1)
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

    def _on_key_down(self, key: InputService.Key):
        if key == InputService.get_action("move.left"):
            self.physics_body.velocity.x = -self._speed
        elif key == InputService.get_action("move.right"):
            self.physics_body.velocity.x = self._speed
        elif key == InputService.get_action("move.up"):
            self.physics_body.velocity.y = -self._speed
        elif key == InputService.get_action("move.down"):
            self.physics_body.velocity.y = self._speed

        self.is_animated = self.physics_body.velocity.magnitude() > 0

    def _on_key_up(self, key: InputService.Key):
        if not InputService.is_input_active(
            InputService.Key.A
        ) and not InputService.is_input_active(InputService.Key.D):
            self.physics_body.velocity.x = 0

        if not InputService.is_input_active(
            InputService.Key.W
        ) and not InputService.is_input_active(InputService.Key.S):
            self.physics_body.velocity.y = 0

        self.is_animated = self.physics_body.velocity.magnitude() > 0

        if not self.is_animated:
            self.current_frame = 0

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = speed
