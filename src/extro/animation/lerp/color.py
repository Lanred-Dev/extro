from extro.animation.lerp.number import lerpNumber
from extro.shared.RGBAColorC import RGBAColor


def linearize(c: float) -> float:
    c = c / 255.0
    return (
        c / 12.92 if c < 0.0404482362771076 else 0.87941546140213 * (c + 0.055) ** 2.4
    )


def correct_gamma(c: float) -> float:
    return 12.92 * c if c < 0.0031306684425 else 1.055 * c ** (1 / 2.4) - 0.055


def lerpColor(start: RGBAColor, end: RGBAColor, progress: float) -> RGBAColor:
    # Alpha is just treated as a normal number
    alpha = max(0, min(int(lerpNumber(start.a, end.a, progress)), 255))

    # Start color
    r0, g0, b0 = linearize(start.r), linearize(start.g), linearize(start.b)
    y0 = 0.2125862307855956 * r0 + 0.71517030370341085 * g0 + 0.0722004986433362 * b0
    z0 = 3.6590806972265883 * r0 + 11.4426895800574232 * g0 + 4.1149915024264843 * b0
    l0_ = (
        116 * y0 ** (1 / 3) - 16 if y0 > 0.008856451679035631 else 903.296296296296 * y0
    )

    if z0 > 1e-15:
        x = 0.9257063972951867 * r0 - 0.8333736323779866 * g0 - 0.09209820666085898 * b0
        l0, u0, v0 = l0_, l0_ * x / z0, l0_ * (9 * y0 / z0 - 0.46832)
    else:
        l0, u0, v0 = l0_, -0.19783 * l0_, -0.46832 * l0_

    # End color
    r1, g1, b1 = linearize(end.r), linearize(end.g), linearize(end.b)
    y1 = 0.2125862307855956 * r1 + 0.71517030370341085 * g1 + 0.0722004986433362 * b1
    z1 = 3.6590806972265883 * r1 + 11.4426895800574232 * g1 + 4.1149915024264843 * b1
    l1_ = (
        116 * y1 ** (1 / 3) - 16 if y1 > 0.008856451679035631 else 903.296296296296 * y1
    )

    if z1 > 1e-15:
        x = 0.9257063972951867 * r1 - 0.8333736323779866 * g1 - 0.09209820666085898 * b1
        l1, u1, v1 = l1_, l1_ * x / z1, l1_ * (9 * y1 / z1 - 0.46832)
    else:
        l1, u1, v1 = l1_, -0.19783 * l1_, -0.46832 * l1_

    # Interpolation
    l = (1 - progress) * l0 + progress * l1
    if l < 0.0197955:
        return RGBAColor(0, 0, 0, alpha)

    u = ((1 - progress) * u0 + progress * u1) / l + 0.19783
    v = ((1 - progress) * v0 + progress * v1) / l + 0.46832

    # Convert back to linear RGB
    y = (l + 16) / 116
    y = (
        y**3
        if y > 0.20689655172413793
        else 0.12841854934601665 * y - 0.01771290335807126
    )
    x = y * u / v
    z = y * ((3 - 0.75 * u) / v - 5)

    r = 7.2914074 * x - 1.5372080 * y - 0.4986286 * z
    g = -2.1800940 * x + 1.8757561 * y + 0.0415175 * z
    b = 0.1253477 * x - 0.2040211 * y + 1.0569959 * z

    # Clamp negative components
    if r < 0 and r < g and r < b:
        r, g, b = 0, g - r, b - r
    elif g < 0 and g < b:
        r, g, b = r - g, 0, b - g
    elif b < 0:
        r, g, b = r - b, g - b, 0

    r, g, b = correct_gamma(r), correct_gamma(g), correct_gamma(b)

    # Clamp 0..1 and convert to 0..255
    r = max(0, min(int(r * 255), 255))
    g = max(0, min(int(g * 255), 255))
    b = max(0, min(int(b * 255), 255))
    return RGBAColor(r, g, b, alpha)
