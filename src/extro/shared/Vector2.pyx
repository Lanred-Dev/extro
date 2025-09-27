cdef class Vector2:
    def __cinit__(self, float x, float y):
        self.x = x
        self.y = y

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    cpdef Vector2 copy(self):
        return Vector2(self.x, self.y)

    cpdef tuple[float, float] to_tuple(self):
        return (self.x, self.y)

    cpdef float magnitude(self):
        return (self.x**2 + self.y**2) ** 0.5

    def dot(self, Vector2 other) -> float:
        return self.__cdot__(other)

    cdef Vector2 __cadd__(self, Vector2 other):
        return Vector2(self.x + other.x, self.y + other.y)

    cdef Vector2 __csub__(self, Vector2 other):
        return Vector2(self.x - other.x, self.y - other.y)

    cdef Vector2 __cmul_vector__(self, Vector2 other):
        return Vector2(self.x * other.x, self.y * other.y)

    cdef Vector2 __cmul_float__(self, float scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    cdef Vector2 __ctruediv_vector__(self, Vector2 other):
        return Vector2(self.x / other.x, self.y / other.y)

    cdef Vector2 __ctruediv_float__(self, float scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    cdef float __cdot__(self, Vector2 other):
        return self.x * other.x + self.y * other.y

    def __add__(self, other: Vector2):
        return self.__cadd__(other)

    def __sub__(self, other: Vector2):
        return self.__csub__(other)

    def __mul__(self, other: Vector2 | float):
        if isinstance(other, Vector2):
            return self.__cmul_vector__(other)
        else:
            return self.__cmul_float__(other)

    def __truediv__(self, other: Vector2 | float):
        if isinstance(other, Vector2):
            return self.__ctruediv_vector__(other)
        else:
            return self.__ctruediv_float__(other)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __lt__(self, other: Vector2) -> bool:
        return self.x < other.x and self.y < other.y

    def __gt__(self, other: Vector2) -> bool:
        return self.x > other.x and self.y > other.y

    def __le__(self, other: Vector2) -> bool:
        return self.x <= other.x and self.y <= other.y

    def __ge__(self, other: Vector2) -> bool:
        return self.x >= other.x and self.y >= other.y

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"

    def __eq__(self, other: Vector2) -> bool:
        return self.x == other.x and self.y == other.y