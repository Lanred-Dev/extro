#include <nanobind/nanobind.h>
#include "Window.hpp"
#include "sokol_gfx.h"
#include "sokol_glue.h"

using namespace nanobind::literals;

bool Window::initialize(Vector2 size, const char *title, bool vSync)
{
    if (!glfwInit())
        return false;

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);

    this->size = size;
    this->title = title;
    this->vSyncEnabled = vSync;
    window = glfwCreateWindow((int)size.x, (int)size.y, title, nullptr, nullptr);

    if (!window)
    {
        glfwTerminate();
        return false;
    }

    glfwMakeContextCurrent(window);
    setVSync(vSync);

    sg_setup(sg_desc{
        .environment = sglue_environment(),
    });

    return true;
}

void Window::terminate()
{
    if (sg_isvalid())
        sg_shutdown();

    if (window)
    {
        glfwDestroyWindow(window);
        window = nullptr;
    }

    glfwTerminate();
}

void Window::setTitle(const char *newTitle)
{
    title = newTitle;
    glfwSetWindowTitle(window, newTitle);
}

void Window::setSize(Vector2 newSize)
{
    size = newSize;
    glfwSetWindowSize(window, (int)size.x, (int)size.y);
}

void Window::setVSync(bool enabled)
{
    vSyncEnabled = enabled;

    if (enabled)
        glfwSwapInterval(1);
    else
        glfwSwapInterval(0);
}

bool Window::render()
{
    bool shouldClose = glfwWindowShouldClose(window);

    // If the window should close dont worry about rendering and return early telling the engine to close
    if (shouldClose)
        return true;
    
    glfwSwapBuffers(window);
    glfwPollEvents();

    return false;
}

void createWindowModule(nanobind::module_ &m)
{
    nanobind::class_<Window>(m, "Window")
        .def(nanobind::init<>())
        .def("initialize", &Window::initialize, "width"_a, "height"_a, "title"_a)
        .def("terminate", &Window::terminate)
        .def("set_title", &Window::setTitle, "title"_a)
        .def("set_size", &Window::setSize, "width"_a, "height"_a)
        .def("render", &Window::render);
}