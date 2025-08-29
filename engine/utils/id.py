import random
import string
from typing import Optional

CHARACTERS = string.ascii_letters + string.digits


def generateID(length: int = 8, prefix: Optional[str] = "") -> str:
    id = "".join(random.choice(CHARACTERS) for _ in range(length))
    return (prefix or "") + id
