#pragma once

#include "GLFW/glfw3.h"
#include "nanobind/nanobind.h"
#include "shared/Vector2.hpp"

namespace Window
{
    bool initialize(Vector2 size, const char *title, bool vSync = false);
    void terminate();
    void setTitle(const char *newTitle);
    const char *getTitle();
    void setSize(Vector2 newSize);
    Vector2* getSize();
    void setVSync(bool enabled);
    bool isVSyncEnabled();
    nanobind::tuple render();
};

void createWindowModule(nanobind::module_ &m);