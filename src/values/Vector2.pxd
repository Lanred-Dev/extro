cdef class Vector2:
    cdef public float x, y
    cpdef Vector2 copy(self)
    cpdef tuple[float, float] to_tuple(self)
    cdef Vector2 __cadd__(self, Vector2 other)
    cdef Vector2 __csub__(self, Vector2 other)
    cdef Vector2 __cmul_vector__(self, Vector2 other)
    cdef Vector2 __cmul_float__(self, float scalar)
    cdef Vector2 __ctruediv_vector__(self, Vector2 other)
    cdef Vector2 __ctruediv_float__(self, float scalar)