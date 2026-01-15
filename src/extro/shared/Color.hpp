#pragma once

#include "nanobind/nanobind.h"

struct Color
{
    uint8_t r, g, b, a;
};

void createColorModule(nanobind::module_ &m);