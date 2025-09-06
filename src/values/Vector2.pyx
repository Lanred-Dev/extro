cdef class Vector2:
    cdef public float x, y

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    cpdef Vector2 copy(self):
        """Return a copy of this vector."""
        return Vector2(self.x, self.y)

    cpdef tuple to_tuple(self):
        """Return a tuple of RGBA values."""
        return (self.x, self.y)

    cdef Vector2 __add(self, Vector2 other):
        return Vector2(self.x + other.x, self.y + other.y)

    cdef Vector2 __sub(self, Vector2 other):
        return Vector2(self.x - other.x, self.y - other.y)

    cdef Vector2 __mul(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    cdef Vector2 __truediv(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other) 

    def __add__(self, other: Vector2):
        """Return a new vector from adding another vector."""
        return self.__add(other)

    def __sub__(self, other: Vector2):
        """Return a new vector from subtracting another vector."""
        return self.__sub(other)

    def __mul__(self, other: Vector2 | float):
        """Return a new vector from multiplying by a scalar or vector."""
        return self.__mul(other)

    def __truediv__(self, other: Vector2 | float):
        """Return a new vector from dividing by a scalar or vector."""
        return self.__truediv(other)

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"