from src.animation.lerp.number import lerpNumber
from src.values.Color import Color


cdef float linearize(float value):
    value = value / 255.0
    return value / 12.92 if value < 0.0404482362771076 else 0.87941546140213 * (value + 0.055) ** 2.4


cdef float correct_gamma(float value):
    return 12.92 * value if value < 0.0031306684425 else 1.055 * value ** (1 / 2.4) - 0.055


cdef object lerpColor(object start, object end, float progress):
    """
    Lerp between a start color and a end color at x.

    This function was adapted from https://github.com/Upbeat-Roblox/fluid/blob/main/src/modules/lerpers/color.lua
    """
    # Alpha is just treated as a normal number
    cdef int alpha = max(0, min(int(lerpNumber(start.a, end.a, progress)), 255))

    cdef double x

    # Start color
    cdef double r0 = linearize(start.r)
    cdef double g0 = linearize(start.g)
    cdef double b0 = linearize(start.b)
    cdef double y0 = 0.2125862307855956 * r0 + 0.71517030370341085 * g0 + 0.0722004986433362 * b0
    cdef double z0 = 3.6590806972265883 * r0 + 11.4426895800574232 * g0 + 4.1149915024264843 * b0
    cdef double l0 = 116 * y0 ** (1 / 3) - 16 if y0 > 0.008856451679035631 else 903.296296296296 * y0
    cdef double u0
    cdef double v0

    if z0 > 1e-15:
        x = 0.9257063972951867 * r0 - 0.8333736323779866 * g0 - 0.09209820666085898 * b0
        u0 = l0 * x / z0
        v0 = l0 * (9 * y0 / z0 - 0.46832)
    else:
        u0 = -0.19783 * l0
        v0 = -0.46832 * l0

    # End color
    cdef double r1 = linearize(end.r)
    cdef double g1 = linearize(end.g)
    cdef double b1 = linearize(end.b)
    cdef double y1 = 0.2125862307855956 * r1 + 0.71517030370341085 * g1 + 0.0722004986433362 * b1
    cdef double z1 = 3.6590806972265883 * r1 + 11.4426895800574232 * g1 + 4.1149915024264843 * b1
    cdef double l1 = 116 * y1 ** (1 / 3) - 16 if y1 > 0.008856451679035631 else 903.296296296296 * y1
    cdef double u1
    cdef double v1
    
    if z1 > 1e-15:
        x = 0.9257063972951867 * r1 - 0.8333736323779866 * g1 - 0.09209820666085898 * b1
        u1 = l1 * x / z1
        v1 = l1 * (9 * y1 / z1 - 0.46832)
    else:
        u1 = -0.19783 * l1
        v1 = -0.46832 * l1

    # Interpolation
    cdef double l = (1 - progress) * l0 + progress * l1

    if l < 0.0197955:
        return Color(0, 0, 0, alpha)

    cdef double u = ((1 - progress) * u0 + progress * u1) / l + 0.19783
    cdef double v = ((1 - progress) * v0 + progress * v1) / l + 0.46832

    # Convert back to linear RGB
    cdef float y = (l + 16) / 116

    if y > 0.20689655172413793:
        y = y**3
    else:
        y = 0.12841854934601665 * y - 0.01771290335807126

    x = y * u / v
    cdef float z = y * ((3 - 0.75 * u) / v - 5)

    cdef double r = 7.2914074 * x - 1.5372080 * y - 0.4986286 * z
    cdef double g = -2.1800940 * x + 1.8757561 * y + 0.0415175 * z
    cdef double b = 0.1253477 * x - 0.2040211 * y + 1.0569959 * z

    # Clamp negative components
    if r < 0 and r < g and r < b:
        r = 0
        g = g - r
        b = b - r
    elif g < 0 and g < b:
        r = r - g
        g = 0
        b = b - g
    elif b < 0:
        r = r - b
        g = g - b
        b = 0

    # Clamp 0..1 and convert to 0..255
    return Color(max(0, min(int(correct_gamma(r) * 255), 255)), max(0, min(int(correct_gamma(g) * 255), 255)), max(0, min(int(correct_gamma(b) * 255), 255)), alpha)
