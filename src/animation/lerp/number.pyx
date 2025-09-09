cdef float lerpNumber(float start, float end, float progress):
    return start + (end - start) * progress
