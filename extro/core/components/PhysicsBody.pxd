from src.shared.Vector2 cimport Vector2

cdef class PhysicsBody:
    cdef int _owner_id
    cdef public float mass
    cdef list _forces
    cdef public Vector2 velocity
    cdef Vector2 _actual_force_velocity
    cdef Vector2 _actual_velocity
    cdef bint _is_anchored
    cpdef apply_force(self, Vector2 force)
