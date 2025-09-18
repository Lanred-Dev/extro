from libc.math cimport sin, cos, M_PI, hypot
from src.values.Vector2 import Vector2

cdef float dot(object a, object b):
    return a.x * b.x + a.y * b.y


cdef object project_polygon(object axis, list[object] vertices):
    """Project all vertices onto an axis and return min/max values."""
    cdef list[float] dots = [0.0] * len(vertices)

    for index in range(len(vertices)):
        dots[index] = dot(vertices[index], axis)

    return Vector2(min(dots), max(dots))


cdef class CollisionMask:
    cdef object _position
    cdef object _size
    cdef float _rotation
    cdef bint _is_dirty
    cdef list[object] _axes
    cdef list[object] _vertices

    def __init__(self, position: object, size: object, rotation: float = 0):
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

        cdef object vertex1
        cdef object vertex2

        for index in range(len(self._vertices)):
            vertex1 = self._vertices[index]
            vertex2 = self._vertices[(index + 1) % len(self._vertices)]
            self._axes.append(Vector2(-(vertex1.y - vertex2.y), vertex1.x - vertex2.x))

    cdef _recompute_if_dirty(self):
        if self._is_dirty == <bint>False:
            return

        self._compute_vertices()
        self._compute_axes()
        self._is_dirty = <bint>False

    cpdef bint collides_with(self, CollisionMask other_collision_mask):
        self._recompute_if_dirty()

        cdef list[object] axes = self._axes + other_collision_mask.axes
        cdef object axis
        cdef float length
        cdef object projection1
        cdef object projection2

        for index in range(len(axes)):
            axis = axes[index]
            length = hypot(<double>axis.x, <double>axis.y)

            if length == 0:
                continue

            # Normalize the axis
            axis.x /= length
            axis.y /= length

            projection1 = project_polygon(axis, self._vertices)
            projection2 = project_polygon(
                axis, other_collision_mask.vertices
            )

            if not (projection1.x <= projection2.y and projection2.x <= projection1.y):
                return <bint>False

        return <bint>True

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Vector2):
        self._position = position
        self._is_dirty = <bint>True

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: Vector2):
        self._size = size
        self._is_dirty = <bint>True

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: float):
        self._rotation = rotation
        self._is_dirty = <bint>True

    @property
    def vertices(self):
        self._recompute_if_dirty()
        return self._vertices

    @property
    def axes(self):
        self._recompute_if_dirty()
        return self._axes