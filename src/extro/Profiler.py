import pyray

from extro.assets.Fonts import Arial

is_enabled: bool = True
_updates: dict[str, list[float]] = {}


def _trim_list(list: list, max_length: int) -> list:
    return list[-max_length:]


def _get_average_of_list(list: list) -> float:
    if len(list) == 0:
        return 0.0

    return sum(list) / len(list)


def _add_update(system_name: str, duration: float):
    if not is_enabled:
        return

    if system_name not in _updates:
        _updates[system_name] = []

    _updates[system_name].append(duration)
    _updates[system_name] = _trim_list(_updates[system_name], 100)


def get_averages() -> dict[str, float]:
    stats = {
        name: _get_average_of_list(durations) for name, durations in _updates.items()
    }
    stats["total"] = sum(stats.values())
    return stats


def get_average_for_system(system_name: str) -> float:
    if system_name not in _updates:
        return 0.0

    return _get_average_of_list(_updates[system_name])


def get_fps() -> float:
    return pyray.get_fps()


def _draw():
    if not is_enabled:
        return

    system_response_times = get_averages()
    stats_width: int = 0
    stats_height: int = 0

    for name, value in system_response_times.items():
        stat_text: str = f"{name}: {value * 1000:.2f} ms"
        stat_size: pyray.Vector2 = pyray.measure_text_ex(Arial(), stat_text, 20, 1)
        stats_width = max(stats_width, int(stat_size.x))
        stats_height += int(stat_size.y) + 5

    stats_width += 10
    pyray.draw_rectangle(
        0,
        0,
        stats_width,
        stats_height + 10,
        (0, 0, 0, 255),
    )

    current_y: int = 5

    for name, value in system_response_times.items():
        pyray.draw_text_ex(
            Arial(),
            f"{name}: {value * 1000:.2f} ms",
            (
                5,
                current_y,
            ),
            20,
            1,
            (255, 255, 255, 255),
        )
        current_y += 25


__all__ = [
    "is_enabled",
    "_add_update",
    "_draw",
    "get_averages",
    "get_average_for_system",
]
