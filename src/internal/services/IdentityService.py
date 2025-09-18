import random
import string

_VALID_ID_CHARACTERS = string.ascii_letters + string.digits


def generate_id(length: int = 8, prefix: str | None = None) -> str:
    """
    Generate a random string ID with optional prefix.

    Example
    -------
    >>> generate_id(6)
    'a1b2c3'
    >>> generate_id(6, prefix='obj_')
    'obj_d4e5f6'
    """

    id = "".join(random.choice(_VALID_ID_CHARACTERS) for _ in range(length))
    return (prefix or "") + id


__all__ = ["generate_id"]
