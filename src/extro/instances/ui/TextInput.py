import pyray

from extro.instances.core.Instance.UI.Clickable import Clickable
from extro.utils.Signal import Signal
import extro.internal.systems.Input as InputSystem
import extro.services.Input as InputService
from extro.instances.ui.Text import Text
from extro.assets.Fonts import Arial
from extro.instances.ui.Font import Font
from extro.shared.Coord import Coord
from extro.shared.RGBAColorC import RGBAColor
from extro.shared.Vector2C import Vector2

BACKSPACE_REPEAT_DEBOUNCE = 0.04
BACKSPACE_REPEAT_START_DELAY = 0.25


class TextInput(Clickable):
    __slots__ = Clickable.__slots__ + (
        "on_input",
        "_is_active",
        "value",
        "placeholder",
        "_on_event_connections",
        "_label",
        "_last_backspace_at",
        "_started_holding_backspace_at",
    )

    value: str
    placeholder: str
    on_input: Signal
    _is_active: bool
    _on_event_connections: list[str] | None
    _label: Text
    _last_backspace_at: float
    _started_holding_backspace_at: float | None

    def __init__(
        self,
        font_size: int,
        font: Font = Arial,
        character_spacing: int = 1,
        placeholder: str = "",
        value: str = "",
        size: Coord = Coord(0, 0, Coord.CoordType.ABSOLUTE),
        text_color: RGBAColor = RGBAColor(255, 255, 255),
        **kwargs,
    ):
        super().__init__(size=size, **kwargs)

        self.value = value
        self.placeholder = placeholder
        self._on_event_connections = None
        self._is_active = False
        self._last_backspace_at = 0
        self._started_holding_backspace_at = None

        self.on_input = Signal()
        self._janitor.add(self.on_input)

        self._label = Text(
            text="",
            font_size=font_size,
            font=font,
            character_spacing=character_spacing,
            scale_size_to_font=True,
            size=size,
            anchor=Vector2(0, 0.5),
            position=Coord(0, 0.5, Coord.CoordType.RELATIVE),
            color=text_color,
            zindex=self.drawable._zindex + 1,
        )
        self.hierarchy.add_child(self._label)
        self._janitor.add(self._label)
        self._update_label()

        self.on_focus_lost.connect(self._on_focus_lost)
        self.on_focus.connect(self._on_focus)

    def _on_focus(self):
        has_capture: bool = InputSystem.request_keyboard_capture(self._id)

        if not has_capture:
            return

        self._is_active = True
        self._on_event_connections = [
            InputSystem.on_event.connect(
                self._on_key_press, InputSystem.SubscriberType.PRESS
            ),
            InputSystem.on_event.connect(
                self._on_backspace_release,
                InputSystem.SubscriberType.RELEASE,
                InputSystem.Keyboard.BACKSPACE,
            ),
            InputSystem.on_event.connect(
                self._on_backspace_repeat,
                InputSystem.SubscriberType.ACTIVE,
                InputSystem.Keyboard.BACKSPACE,
            ),
        ]

    def _on_focus_lost(self):
        if not self._is_active:
            return

        self._is_active = False
        InputSystem.release_keyboard_capture()

        if self._on_event_connections:
            for connection_id in self._on_event_connections:
                InputSystem.on_event.disconnect(connection_id)

            self._on_event_connections = None

    def _on_backspace_repeat(self, _):
        now: float = pyray.get_time()

        if (
            now - self._last_backspace_at < BACKSPACE_REPEAT_DEBOUNCE
            or self._started_holding_backspace_at is None
            or now - self._started_holding_backspace_at < BACKSPACE_REPEAT_START_DELAY
        ):
            return

        self.value = self.value[:-1]
        self._update_label()
        self.on_input.fire(self.value)
        self._last_backspace_at = now

    def _on_backspace_release(self, _):
        self._started_holding_backspace_at = None

    def _on_key_press(self, input: InputSystem.Keyboard, *_):
        # This could be a mouse input so just to make sure
        if input not in InputSystem.Keyboard:
            return

        match input:
            case InputSystem.Keyboard.BACKSPACE:
                self.value = self.value[:-1]
                self._started_holding_backspace_at = pyray.get_time()
            case InputSystem.Keyboard.ENTER | InputSystem.Keyboard.ESCAPE:
                self._on_focus_lost()
            case _:
                self.value += (
                    InputService.keycode_to_character(
                        input,
                        (
                            (InputSystem.KeyboardModifiers.SHIFT,)
                            if InputSystem.active_inputs[InputSystem.Keyboard.SHIFT]
                            else None
                        ),
                    )
                    or ""
                )

        self._update_label()
        self.on_input.fire(self.value)

    def _update_label(self):
        self._label.text = self.value if len(self.value) > 0 else self.placeholder

    def draw(self):
        pyray.draw_rectangle_pro(
            (*self.transform._actual_position, *self.transform._actual_size),
            self.transform._position_offset,
            self.transform._rotation,
            self.drawable.color.to_tuple(),
        )
