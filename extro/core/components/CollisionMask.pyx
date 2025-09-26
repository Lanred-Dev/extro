from libc.math cimport sin, cos, M_PI, hypot

from extro.shared.Vector2 cimport Vector2

cdef float dot(Vector2 a, Vector2 b):
    return a.x * b.x + a.y * b.y


cdef Vector2 project_polygon(Vector2 axis, list[Vector2] vertices):
    """Project all vertices onto an axis and return min/max values."""
    cdef int length = len(vertices)
    cdef list[float] dots = [0.0] * length

    for index in range(length):
        dots[index] = dot(vertices[index], axis)
    
    cdef float min_dot = dots[0]
    cdef float max_dot = dots[0]

    for index in range(1, length):
        if dots[index] < min_dot:
            min_dot = dots[index]

        if dots[index] > max_dot:
            max_dot = dots[index]
    
    return Vector2(min_dot, max_dot)



cdef class CollisionMask:
    cdef Vector2 _position
    cdef Vector2 _size
    cdef float _rotation
    cdef bint _is_dirty
    cdef list[Vector2] _axes
    cdef list[Vector2] _vertices

    def __cinit__(self, Vector2 position, Vector2 size, float rotation):
        self._position = position
        self._size = size
        self._rotation = rotation
        self._vertices = []
        self._is_dirty = <bint>True

    def __init__(self, position: Vector2, size: Vector2, rotation: float):
        self._position = position
        self._size = size
        self._rotation = rotation
        self._vertices = []
        self._is_dirty = <bint>True

    cdef _compute_vertices(self):
        cdef float half_width = self._size.x / 2
        cdef float half_height = self._size.y / 2
        cdef double rotation = self._rotation * M_PI / 180
        cdef list[list[float]] local_vertices = [[-half_width, -half_height], [half_width, -half_height], [half_width, half_height], [-half_width, half_height]]
        cdef float vertex_x
        cdef float vertex_y
        cdef float cos_rotation = cos(rotation)
        cdef float sin_rotation = sin(rotation)
        cdef Vector2 vertex

        self._vertices = []

        for index in range(4):
            vertex_x = local_vertices[index][0]
            vertex_y = local_vertices[index][1]
            
            self._vertices.append(
                Vector2(
                    self._position.x + vertex_x * cos_rotation - vertex_y * sin_rotation,
                    self._position.y + vertex_x * sin_rotation + vertex_y * cos_rotation
                )
            )

    cdef _compute_axes(self):
        self._axes = []

        cdef Vector2 vertex1
        cdef Vector2 vertex2
        cdef Vector2 axis
        cdef float axis_length

        for index in range(len(self._vertices)):
            vertex1 = self._vertices[index]
            vertex2 = self._vertices[(index + 1) % len(self._vertices)]
            
            axis = Vector2(-(vertex1.y - vertex2.y), vertex1.x - vertex2.x)
            axis_length = hypot(<double>axis.x, <double>axis.y)

            if axis_length == 0:
                continue

            # Normalize the axis
            axis.x /= axis_length
            axis.y /= axis_length

            self._axes.append(axis)

    cdef _recompute_if_dirty(self):
        if self._is_dirty == <bint>False:
            return

        self._compute_vertices()
        self._compute_axes()
        self._is_dirty = <bint>False

    cpdef bint collides_with(self, CollisionMask other_collision_mask):
        self._recompute_if_dirty()

        cdef list[Vector2] axes = self._axes + other_collision_mask.axes
        cdef Vector2 axis
        cdef Vector2 projection1
        cdef Vector2 projection2

        for index in range(len(axes)):
            axis = axes[index]
            projection1 = project_polygon(axis, self._vertices)
            projection2 = project_polygon(axis, other_collision_mask.vertices)

            if not (projection1.x <= projection2.y and projection2.x <= projection1.y):
                return <bint>False

        return <bint>True

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, position: Vector2):
        self._position = position
        self._is_dirty = <bint>True

    @property
    def size(self) -> Vector2:
        return self._size

    @size.setter
    def size(self, size: Vector2):
        self._size = size
        self._is_dirty = <bint>True

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: float):
        self._rotation = rotation
        self._is_dirty = <bint>True

    @property
    def vertices(self) -> list[Vector2]:
        self._recompute_if_dirty()
        return self._vertices

    @property
    def axes(self) -> list[Vector2]:
        self._recompute_if_dirty()
        return self._axes