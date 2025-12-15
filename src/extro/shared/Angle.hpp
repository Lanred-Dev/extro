#pragma once

#include <cmath>

const float DEGREES_TO_RAD = (atan(1.0f) * 4.0f) / 180.0f;
const float RAD_TO_DEGREES = 1.0f / DEGREES_TO_RAD;

struct Angle
{
    float radians;
    float degrees;

    Angle() : radians(0.0f), degrees(0.0f) {}
    Angle(float rad) : radians(rad), degrees(rad * RAD_TO_DEGREES) {}

    void setRadians(float value)
    {
        radians = value;
        degrees = value * RAD_TO_DEGREES;
    }

    void setDegrees(float value)
    {
        degrees = value;
        radians = value * DEGREES_TO_RAD;
    }

    Angle copy() const
    {
        return Angle(radians);
    }

    Angle operator+(const Angle &other) const
    {
        return Angle(radians + other.radians);
    }

    Angle operator-(const Angle &other) const
    {
        return Angle(radians - other.radians);
    }

    Angle operator*(float scalar) const
    {
        return Angle(radians * scalar);
    }

    friend Angle operator*(const Angle &a, const Angle &b)
    {
        return Angle(a.radians * b.radians);
    }

    Angle operator/(float scalar) const
    {
        return Angle(radians / scalar);
    }

    friend Angle operator/(const Angle &a, const Angle &b)
    {
        return Angle(a.radians / b.radians);
    }

    Angle &operator+=(const Angle &other)
    {
        setRadians(radians + other.radians);
        return *this;
    }

    Angle &operator-=(const Angle &other)
    {
        setRadians(radians - other.radians);
        return *this;
    }

    Angle &operator*=(float scalar)
    {
        setRadians(radians * scalar);
        return *this;
    }

    Angle &operator/=(float scalar)
    {
        setRadians(radians / scalar);
        return *this;
    }

    Angle operator-() const
    {
        return Angle(-radians);
    }

    bool operator==(const Angle &other) const
    {
        return radians == other.radians;
    }

    bool operator!=(const Angle &other) const
    {
        return !(*this == other);
    }

    bool operator<(const Angle &other) const
    {
        return radians < other.radians;
    }

    bool operator<=(const Angle &other) const
    {
        return radians <= other.radians;
    }

    bool operator>(const Angle &other) const
    {
        return radians > other.radians;
    }

    bool operator>=(const Angle &other) const
    {
        return radians >= other.radians;
    }
};