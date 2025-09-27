from extro.shared.Vector2 cimport Vector2

cdef class PhysicsBody:
    cdef int _owner_id
    cdef float _mass
    cdef float _actual_mass
    cdef list _forces
    cdef public Vector2 desired_velocity
    cdef Vector2 _physics_velocity
    cdef Vector2 _actual_force_velocity
    cdef Vector2 _actual_velocity
    cdef bint _is_anchored
    cdef public float restitution
    cpdef apply_force(self, Vector2 force)
    cdef _recalculate_actual_mass(self)