cmake_minimum_required(VERSION 3.15...3.27)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
project(extro LANGUAGES CXX)

set(GLFW_BUILD_DOCS OFF CACHE BOOL "" FORCE)
set(GLFW_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(GLFW_INSTALL OFF CACHE BOOL "" FORCE)
add_subdirectory(libs/glfw)

if (CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()

find_package(Python COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

# This functions builds a cpp module and places it, along with its typing files, where it belongs.
function(add_nanobind_module MODULE_NAME CPP_PATH)
    nanobind_add_module(${MODULE_NAME} STABLE_ABI ${CPP_PATH} ${ARGN})

    get_filename_component(CPP_DIR_REL "${CPP_PATH}" DIRECTORY)
    
    if(CPP_DIR_REL STREQUAL "")
        set(CPP_DIR_ABS "${CMAKE_SOURCE_DIR}")
    else()
        set(CPP_DIR_ABS "${CMAKE_SOURCE_DIR}/${CPP_DIR_REL}")
    endif()

    set_target_properties(${MODULE_NAME} PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/extro"
    )

    add_custom_command(TARGET ${MODULE_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E echo "Copying ${MODULE_NAME} .pyd to source directory"
        COMMAND ${CMAKE_COMMAND} -E copy
            $<TARGET_FILE:${MODULE_NAME}>
            "${CPP_DIR_ABS}/$<TARGET_FILE_NAME:${MODULE_NAME}>"
        COMMAND ${CMAKE_COMMAND} -E echo "Generating .pyi stub for ${MODULE_NAME}"
        COMMAND ${Python_EXECUTABLE} -c 
            "import sys; sys.path.append('${CPP_DIR_ABS}'); from nanobind import stubgen; stubgen.main(['-m', '${MODULE_NAME}', '-o', '${CPP_DIR_ABS}/${MODULE_NAME}.pyi'])"
        VERBATIM
    )

    get_filename_component(PKG_REL_DIR "${CPP_PATH}" DIRECTORY)
    file(RELATIVE_PATH PKG_REL_DIR "${CMAKE_SOURCE_DIR}/src/extro" "${CPP_DIR_ABS}")

    install(TARGETS ${MODULE_NAME}
        LIBRARY DESTINATION "extro/${PKG_REL_DIR}"
        ARCHIVE DESTINATION "extro/${PKG_REL_DIR}"
        RUNTIME DESTINATION "extro/${PKG_REL_DIR}")
endfunction()

add_nanobind_module(bindings 
    src/extro/bindings.cpp
    src/extro/internal/sokol_implementation.cpp
    src/extro/Window.cpp
    src/extro/shared/Vector2.cpp
    src/extro/shared/Color.cpp
    src/extro/shared/Angle.cpp
)
target_include_directories(bindings PUBLIC 
    "${PROJECT_SOURCE_DIR}/libs/glfw/include"
    "${PROJECT_SOURCE_DIR}/libs/sokol"
    "${PROJECT_SOURCE_DIR}/src/extro"
)
target_link_libraries(bindings PRIVATE glfw sokol)