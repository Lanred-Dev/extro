#include <string>
#include "Color.hpp"

using namespace nanobind::literals;

void createColorModule(nanobind::module_ &m)
{
    nanobind::class_ cColor = nanobind::class_<Color>(m, "Color");
    cColor.doc() = R"(
    Class representing a color with red, green, blue, and alpha components.

    Attributes:
         - r (int):
            Red component (0-255).
         - g (int):
            Green component (0-255).
         - b (int):
            Blue component (0-255).
         - a (int):
            Alpha component (0-255), defaults to 255 (opaque).
    )";
    cColor
        .def(nanobind::init<>())
        .def(nanobind::init<uint8_t, uint8_t, uint8_t, uint8_t>(), "r"_a, "g"_a, "b"_a, "a"_a = 255)
        .def_prop_rw("r", [](Color &color)
                     { return color.r; }, [](Color &color, uint8_t value)
                     { color.r = value; })
        .def_prop_rw("g", [](Color &color)
                     { return color.g; }, [](Color &color, uint8_t value)
                     { color.g = value; })
        .def_prop_rw("b", [](Color &color)
                     { return color.b; }, [](Color &color, uint8_t value)
                     { color.b = value; })
        .def_prop_rw("a", [](Color &color)
                     { return color.a; }, [](Color &color, uint8_t value)
                     { color.a = value; })
        .def("__repr__", [](const Color &color)
             { return nanobind::str(std::string("Color(r=" + std::to_string(color.r) +
                                                " g=" + std::to_string(color.g) +
                                                " b=" + std::to_string(color.b) +
                                                " a=" + std::to_string(color.a) + ")")
                                        .c_str()); });
}