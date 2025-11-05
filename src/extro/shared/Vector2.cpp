#include <nanobind/nanobind.h>
#include <nanobind/operators.h>
#include <string>
#include <cmath>

using namespace nanobind::literals;

struct Vector2
{
    float x, y;

    Vector2() : x(0), y(0) {}
    Vector2(float x, float y) : x(x), y(y) {}

    nanobind::tuple toTuple() const
    {
        return nanobind::make_tuple(x, y);
    }

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

NB_MODULE(Vector2, m)
{
    nanobind::class_<Vector2>(m, "Vector2")
        .def(nanobind::init<>())
        .def(nanobind::init<float, float>(), "x"_a, "y"_a)
        .def_prop_rw("x", [](Vector2 &vector)
                     { return vector.x; }, [](Vector2 &vector, float value)
                     { vector.x = value; })
        .def_prop_rw("y", [](Vector2 &vector)
                     { return vector.y; }, [](Vector2 &vector, float value)
                     { vector.y = value; })
        .def("magnitude", &Vector2::magnitude)
        .def("dot", &Vector2::dot, "other"_a)
        .def("to_tuple", &Vector2::toTuple)
        .def("copy", &Vector2::copy)
        .def(nanobind::self + nanobind::self)
        .def(nanobind::self - nanobind::self)
        .def(nanobind::self * float())
        .def(nanobind::self * nanobind::self)
        .def(nanobind::self / float())
        .def(nanobind::self / nanobind::self)
        .def(nanobind::self += nanobind::self)
        .def(nanobind::self -= nanobind::self)
        .def(nanobind::self *= float())
        .def(nanobind::self /= float())
        .def("__eq__", [](const Vector2 &self, nanobind::object other)
             {
                if (!nanobind::isinstance<Vector2>(other)) return false;
                return self == nanobind::cast<Vector2>(other); })
        .def("__ne__", [](const Vector2 &self, nanobind::object other)
             {
                if (!nanobind::isinstance<Vector2>(other)) return true;
                return self != nanobind::cast<Vector2>(other); })
        .def(nanobind::self < nanobind::self)
        .def(nanobind::self <= nanobind::self)
        .def(nanobind::self > nanobind::self)
        .def(nanobind::self >= nanobind::self)
        .def("__neg__", [](const Vector2 &self)
             { return -self; })
        .def("__repr__", [](const Vector2 &vector)
             { return nanobind::str(std::string("Vector2(x=" + std::to_string(vector.x) +
                                                " y=" + std::to_string(vector.y) + ")")
                                        .c_str()); });
}