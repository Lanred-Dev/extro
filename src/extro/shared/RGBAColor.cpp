#include <nanobind/nanobind.h>
#include <nanobind/operators.h>
#include <string>

using namespace nanobind::literals;

struct RGBAColor
{
    uint8_t r, g, b, a;
    nanobind::list list;

    RGBAColor() : r(0), g(0), b(0), a(255)
    {
        list = nanobind::list();
        list.append(r);
        list.append(g);
        list.append(b);
        list.append(a);
    }
    RGBAColor(uint8_t r, uint8_t g, uint8_t b, uint8_t a = 255)
        : r(r), g(g), b(b), a(a)
    {
        list = nanobind::list();
        list.append(r);
        list.append(g);
        list.append(b);
        list.append(a);
    }

    void recompute_list()
    {
        list[0] = r;
        list[1] = g;
        list[2] = b;
        list[3] = a;
    }
};

NB_MODULE(RGBAColor, m)
{
    nanobind::class_<RGBAColor>(m, "RGBAColor")
        .def(nanobind::init<>())
        .def(nanobind::init<uint8_t, uint8_t, uint8_t, uint8_t>(), "r"_a, "g"_a, "b"_a, "a"_a = 255)
        .def_prop_rw("r", [](RGBAColor &color)
                     { return color.r; }, [](RGBAColor &color, uint8_t value)
                     { color.r = value; color.recompute_list(); })
        .def_prop_rw("g", [](RGBAColor &color)
                     { return color.g; }, [](RGBAColor &color, uint8_t value)
                     { color.g = value; color.recompute_list(); })
        .def_prop_rw("b", [](RGBAColor &color)
                     { return color.b; }, [](RGBAColor &color, uint8_t value)
                     { color.b = value; color.recompute_list(); })
        .def_prop_rw("a", [](RGBAColor &color)
                     { return color.a; }, [](RGBAColor &color, uint8_t value)
                     { color.a = value; color.recompute_list(); })
        .def_prop_ro("list", [](RGBAColor &color)
                     { return color.list; })
        .def("__repr__", [](const RGBAColor &color)
             { return nanobind::str(std::string("RGBAColor(r=" + std::to_string(color.r) +
                                                " g=" + std::to_string(color.g) +
                                                " b=" + std::to_string(color.b) +
                                                " a=" + std::to_string(color.a) + ")")
                                        .c_str()); });
}