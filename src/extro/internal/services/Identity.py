import random
import string
from enum import Enum


class IDCharacters(Enum):
    ALL = string.ascii_letters + string.digits
    ALPHABETIC = string.ascii_letters
    NUMERIC = string.digits


last_numeric_id: int = 0


def generate_id(
    length: int, prefix: str | None = None, use: IDCharacters = IDCharacters.ALL
) -> str:
    """
    Generate a random string ID with optional prefix.

    Example
    -------
    >>> generate_id(6)
    'a1b2c3'
    >>> generate_id(6, prefix='obj_')
    'obj_d4e5f6'
    """
    id: str = "".join(random.choice(use.value) for _ in range(length))
    return f"{prefix or ''}{id}"


def generate_ordered_numeric_id() -> int:
    """Generate a unique, incrementing numeric ID."""
    global last_numeric_id
    last_numeric_id += 1
    return last_numeric_id
