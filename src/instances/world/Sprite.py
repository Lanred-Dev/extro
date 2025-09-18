import pyray
import time

from src.instances.core.DrawableInstance import DrawableInstance
from src.values.Vector2 import Vector2
import src.internal.Console as Console


class Sprite(DrawableInstance):
    __slots__ = (
        "_texture",
        "_texture_rect",
        "_texture_source",
        "_frame_size",
        "_is_animated",
        "_current_frame",
        "_frame_time",
        "_last_frame_at",
    )

    _texture: pyray.Texture
    _texture_rect: pyray.Rectangle
    _texture_source: pyray.Rectangle
    _frame_size: Vector2
    _is_animated: bool
    _current_frame: int
    _frame_time: float
    _last_frame_at: float
    _frame_count: int

    def __init__(
        self,
        image_path: str,
        is_animated: bool = False,
        frame_size: Vector2 = Vector2(0, 0),
        frame_time: float = 0.1,
        starting_frame: int = 0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._texture = pyray.load_texture(image_path)
        self._texture_rect = pyray.Rectangle(
            self._actual_position.x,
            self._actual_position.y,
            self._actual_size.x,
            self._actual_size.y,
        )

        if is_animated:
            self._frame_size = frame_size
        else:
            self._frame_size = Vector2(self._texture.width, self._texture.height)

        self._texture_source = pyray.Rectangle(
            self._frame_size.x * starting_frame,
            self._frame_size.y * starting_frame,
            self._frame_size.x,
            self._frame_size.y,
        )

        self._is_animated = is_animated
        self._current_frame = starting_frame
        self._frame_count = (
            int(self._texture.width // self._frame_size.x) if is_animated else 1
        )
        self._frame_time = frame_time
        self._last_frame_at = time.time()

        self._janitor.add(pyray.unload_texture, self._texture)

    def draw(self):
        if self._is_animated:
            now = time.time()

            if now - self._last_frame_at >= self._frame_time:
                self._set_frame((self._current_frame + 1) % self._frame_count)
                self._last_frame_at = now

        pyray.draw_texture_pro(
            self._texture,
            self._texture_source,
            self._texture_rect,
            self._render_origin.to_tuple(),
            self._rotation,
            self._color.to_tuple(),
        )

    def _apply_size(self):
        self._texture_rect.width = self._actual_size.x
        self._texture_rect.height = self._actual_size.y
        super()._apply_size()

    def _apply_position(self):
        self._texture_rect.x = self._actual_position.x
        self._texture_rect.y = self._actual_position.y
        super()._apply_position()

    @property
    def is_animated(self) -> bool:
        return self._is_animated

    @is_animated.setter
    def is_animated(self, is_animated: bool):
        self._is_animated = is_animated

    @property
    def current_frame(self) -> int:
        return self._current_frame

    @current_frame.setter
    def current_frame(self, frame: int):
        if frame < 0 or frame >= self._frame_count:
            Console.log(
                f"Frame {frame} is out of bounds for this sprite (0-{self._frame_count - 1})",
                Console.LogType.ERROR,
            )
            return

        self._set_frame(frame)

    def _set_frame(self, frame: int):
        self._current_frame = frame
        self._texture_source.x = frame * self._frame_size.x
