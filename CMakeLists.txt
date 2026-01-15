if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

cmake_minimum_required(VERSION 3.15...3.27)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
project(extro LANGUAGES CXX)

# GLFW configuration
set(GLFW_BUILD_DOCS OFF CACHE BOOL "" FORCE)
set(GLFW_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(GLFW_INSTALL OFF CACHE BOOL "" FORCE)
add_subdirectory(vendor/glfw)

# Python configuration
if (CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()
find_package(Python COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

# nanobind configuration
add_subdirectory(vendor/nanobind)

# Build targets
nanobind_add_module(bindings STABLE_ABI
    src/extro/bindings.cpp
    src/extro/internal/sokol_implementation.cpp
    src/extro/internal/systems/Render/Renderer.cpp
    src/extro/Window.cpp
    src/extro/shared/Vector2.cpp
    src/extro/shared/Color.cpp
    src/extro/shared/Angle.cpp
)

set(BIN_DIR "${CMAKE_SOURCE_DIR}/src/extro")

set_target_properties(bindings PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${BIN_DIR}"
    LIBRARY_OUTPUT_DIRECTORY_RELEASE "${BIN_DIR}"
    LIBRARY_OUTPUT_DIRECTORY_DEBUG "${BIN_DIR}"
)

nanobind_add_stub(
    bindings_stub
    MODULE extro.bindings  
    OUTPUT_PATH "${CMAKE_SOURCE_DIR}/src" 
    OUTPUT
        "${CMAKE_SOURCE_DIR}/src/extro/bindings/__init__.pyi"
        "${CMAKE_SOURCE_DIR}/src/extro/bindings/Window.pyi"
        "${CMAKE_SOURCE_DIR}/src/extro/bindings/Renderer.pyi"
    PYTHON_PATH "${CMAKE_SOURCE_DIR}/src"
    DEPENDS bindings
    RECURSIVE
)

target_include_directories(bindings PUBLIC 
    "${PROJECT_SOURCE_DIR}/vendor/glfw/include"
    "${PROJECT_SOURCE_DIR}/vendor/sokol"
    "${PROJECT_SOURCE_DIR}/vendor/sokol_gp"
    "${BIN_DIR}"
)
target_link_libraries(bindings PRIVATE glfw)

install(TARGETS bindings
    LIBRARY DESTINATION "extro"
    ARCHIVE DESTINATION "extro"
    RUNTIME DESTINATION "extro"
)