#pragma once

#include <string>
#include <cmath>

struct Vector2
{
    float x, y;

    Vector2() : x(0), y(0) {}
    Vector2(float x, float y) : x(x), y(y) {}

    Vector2 copy() const
    {
        return Vector2(x, y);
    }

    float magnitude() const
    {
        return std::sqrt(x * x + y * y);
    }

    float dot(const Vector2 &other) const
    {
        return x * other.x + y * other.y;
    }

    Vector2 operator+(const Vector2 &other) const
    {
        return Vector2(x + other.x, y + other.y);
    }

    Vector2 operator-(const Vector2 &other) const
    {
        return Vector2(x - other.x, y - other.y);
    }

    Vector2 operator*(float scalar) const
    {
        return Vector2(x * scalar, y * scalar);
    }

    friend Vector2 operator*(const Vector2 &a, const Vector2 &b)
    {
        return Vector2(a.x * b.x, a.y * b.y);
    }

    Vector2 operator/(float scalar) const
    {
        return Vector2(x / scalar, y / scalar);
    }

    friend Vector2 operator/(const Vector2 &a, const Vector2 &b)
    {
        return Vector2(a.x / b.x, a.y / b.y);
    }

    Vector2 &operator+=(const Vector2 &other)
    {
        x += other.x;
        y += other.y;
        return *this;
    }

    Vector2 &operator-=(const Vector2 &other)
    {
        x -= other.x;
        y -= other.y;
        return *this;
    }

    Vector2 &operator*=(float scalar)
    {
        x *= scalar;
        y *= scalar;
        return *this;
    }

    Vector2 &operator/=(float scalar)
    {
        x /= scalar;
        y /= scalar;
        return *this;
    }

    Vector2 operator-() const
    {
        return Vector2(-x, -y);
    }

    bool operator==(const Vector2 &other) const
    {
        return x == other.x && y == other.y;
    }

    bool operator!=(const Vector2 &other) const
    {
        return !(*this == other);
    }

    bool operator<(const Vector2 &other) const
    {
        return magnitude() < other.magnitude();
    }

    bool operator<=(const Vector2 &other) const
    {
        return magnitude() <= other.magnitude();
    }

    bool operator>(const Vector2 &other) const
    {
        return magnitude() > other.magnitude();
    }

    bool operator>=(const Vector2 &other) const
    {
        return magnitude() >= other.magnitude();
    }
};
