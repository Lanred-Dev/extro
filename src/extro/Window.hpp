#pragma once

#include <GLFW/glfw3.h>
#include "shared/Vector2.hpp"

class Window
{
public:
    bool initialize(Vector2 size, const char *title, bool vSync = false);
    void terminate();
    void setTitle(const char *newTitle);
    const char *getTitle() { return title; }
    void setSize(Vector2 newSize);
    Vector2 getSize() { return size; }
    void setVSync(bool enabled);
    bool isVSyncEnabled() { return vSyncEnabled; }
    bool render();

private:
    GLFWwindow *window = nullptr;
    // Having states be private so that developers are forced to use the getter/setter
    bool vSyncEnabled = false;
    Vector2 size = Vector2(800, 600);
    const char *title = "extro";
};

void createWindowModule(nanobind::module_ &m);