#include <nanobind/nanobind.h>
#include <nanobind/operators.h>
#include <string>
#include "Angle.hpp"

using namespace nanobind::literals;

NB_MODULE(Angle, m)
{
    m.def("from_degrees", [](float degrees)
          {
              Angle angle;
              angle.setDegrees(degrees);
              return angle; }, "degrees"_a);

    m.def("from_radians", [](float radians)
          {
              Angle angle;
              angle.setRadians(radians);
              return angle; }, "radians"_a);

    nanobind::class_<Angle>(m, "Angle")
        .def(nanobind::init<>())
        .def(nanobind::init<float>(), "radians"_a)
        .def_prop_rw("radians", [](Angle &angle)
                     { return angle.radians; }, [](Angle &angle, float newRadians)
                     { angle.setRadians(newRadians); })
        .def_prop_rw("degrees", [](Angle &angle)
                     { return angle.degrees; }, [](Angle &angle, float newDegrees)
                     { angle.setDegrees(newDegrees); })
        .def("copy", &Angle::copy)
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
        .def("__eq__", [](const Angle &self, nanobind::object other)
             {
                if (!nanobind::isinstance<Angle>(other)) return false;
                return self == nanobind::cast<Angle>(other); })
        .def("__ne__", [](const Angle &self, nanobind::object other)
             {
                if (!nanobind::isinstance<Angle>(other)) return true;
                return self != nanobind::cast<Angle>(other); })
        .def(nanobind::self < nanobind::self)
        .def(nanobind::self <= nanobind::self)
        .def(nanobind::self > nanobind::self)
        .def(nanobind::self >= nanobind::self)
        .def("__neg__", [](const Angle &angle)
             { return -angle; })
        .def("__repr__", [](const Angle &angle)
             { return nanobind::
                   str(std::
                           string("Angle(radians=" + std::to_string(angle.radians) +
                                  " degrees=" + std::to_string(angle.degrees) + ")")
                               .c_str()); });
}