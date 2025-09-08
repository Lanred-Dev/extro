from typing import Tuple

class Color:
    r: int
    g: int
    b: int
    a: int

    def __init__(self, r: int, g: int, b: int, a: int = 255): ...
    def to_tuple(self) -> Tuple[int, int, int, int]: ...
    def __str__(self) -> str: ...
