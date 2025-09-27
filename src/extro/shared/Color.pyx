cdef class Color:
    cdef public unsigned char r, g, b, a

    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.r = <unsigned char>r
        self.g = <unsigned char>g
        self.b = <unsigned char>b
        self.a = <unsigned char>a

    cpdef tuple[int, int, int, int] to_tuple(self):
        return (self.r, self.g, self.b, self.a)

    def __str__(self):
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"