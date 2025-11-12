#include <nanobind/nanobind.h>
#include <nanobind/operators.h>
#include <string>
#include "Vector2.hpp"

using namespace nanobind::literals;

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
        .def("to_tuple", [](const Vector2 &vector)
             { return nanobind::make_tuple(vector.x, vector.y); })
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