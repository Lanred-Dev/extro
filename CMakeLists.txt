cmake_minimum_required(VERSION 3.15...3.27)
project(extro)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Python 3.14 COMPONENTS Interpreter Development REQUIRED)
find_package(nanobind CONFIG REQUIRED)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

function(add_nanobind_module MODULE_NAME CPP_PATH PY_DEST)
    nanobind_add_module(${MODULE_NAME} STABLE_ABI ${CPP_PATH})
    install(TARGETS ${MODULE_NAME}
            LIBRARY DESTINATION ${PY_DEST})
    add_custom_command(TARGET ${MODULE_NAME} POST_BUILD
        COMMAND ${Python_EXECUTABLE} -c 
            "import sys; sys.path.append('${CMAKE_SOURCE_DIR}/src'); from nanobind import stubgen; stubgen.main(['-m', '${MODULE_NAME}', '-o', 'src/${PY_DEST}/${MODULE_NAME}.pyi'])"
    )
endfunction()

add_nanobind_module(Vector2C src/extro/shared/Vector2C.cpp extro/shared)
add_nanobind_module(RGBAColorC src/extro/shared/RGBAColorC.cpp extro/shared)
add_nanobind_module(CollisionMask src/extro/internal/systems/Collision/CollisionMask.cpp extro/internal/systems/Collision)
