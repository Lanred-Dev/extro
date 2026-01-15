#include "Window.hpp"
#include "internal/systems/Render/Renderer.hpp"

using namespace nanobind::literals;

GLFWwindow *window = nullptr;
bool vSyncEnabled = false;
Vector2 size = Vector2(800, 600);
const char *title = "extro";

bool Window::initialize(Vector2 newSize, const char *newTitle, bool newVSyncEnabled)
{
    if (!glfwInit())
        return false;

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);

    size = newSize;
    title = newTitle;
    window = glfwCreateWindow((int)size.x, (int)size.y, title, nullptr, nullptr);

    if (!window)
    {
        Window::terminate();
        return false;
    }

    bool rendererInitialized = Renderer::initialize();

    if (!rendererInitialized)
    {
        Window::terminate();
        return false;
    }

    glfwMakeContextCurrent(window);
    setVSync(vSyncEnabled);

    return true;
}

void Window::terminate()
{
    Renderer::terminate();

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

nanobind::tuple Window::render()
{
    bool shouldClose = glfwWindowShouldClose(window);

    // If the window should close dont worry about rendering and return early telling the engine to close
    if (shouldClose)
        return nanobind::make_tuple(true, 0.0);

    double delta = Renderer::render();

    glfwSwapBuffers(window);
    glfwPollEvents();

    return nanobind::make_tuple(false, delta);
}

Vector2 *Window::getSize()
{
    return &size;
}

const char *Window::getTitle()
{
    return title;
}

bool Window::isVSyncEnabled()
{
    return vSyncEnabled;
}

void createWindowModule(nanobind::module_ &m)
{
    nanobind::module_ mWindow = m.def_submodule("Window");
    mWindow.doc() = R"(
    Core window bindings for extro.

    This module provides functions to initialize and manage the application window,
    including setting the title, size, and VSync options. It uses GLFW under the hood for window management.

    Methods:
        - initialize(size: Vector2, title: str, vSyncEnabled: bool) -> bool
            Initializes the window with the specified size, title, and VSync option.
            Returns True if initialization was successful, False otherwise.
        - terminate() -> None
            Terminates the window and cleans up resources.
        - set_title(title: str) -> None
            Sets the window title to the specified string.
        - set_size(size: Vector2) -> None
            Sets the window size to the specified Vector2 dimensions.
        - render() -> tuple[bool, double]
            Renders the current frame. Returns True if the window should close, False otherwise.
    )";
    mWindow
        .def("initialize", &Window::initialize, "size"_a, "title"_a, "vSyncEnabled"_a)
        .def("terminate", &Window::terminate)
        .def("set_title", &Window::setTitle, "title"_a)
        .def("set_size", &Window::setSize, "size"_a)
        .def("render", &Window::render);
}