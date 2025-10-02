cmake_minimum_required(VERSION 3.15...3.27)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
project(extro)

if (CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()

find_package(Python 3.13 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

function(add_nanobind_module MODULE_NAME CPP_PATH)
    # Add the nanobind module
    nanobind_add_module(${MODULE_NAME} STABLE_ABI ${CPP_PATH})

    # Get the directory containing the .cpp file (e.g., "" or "test")
    get_filename_component(CPP_DIR_REL "${CPP_PATH}" DIRECTORY)
    
    # Set the absolute directory path where the Pyd/Pyi should go
    if(CPP_DIR_REL STREQUAL "")
        # For root files (my_ext.cpp), use the project source root
        set(CPP_DIR_ABS "${CMAKE_SOURCE_DIR}")
    else()
        # For files in subdirectories (test/a.cpp), combine source root and relative directory
        set(CPP_DIR_ABS "${CMAKE_SOURCE_DIR}/${CPP_DIR_REL}")
    endif()

    # Define paths using the absolute directory
    set(COPIED_PYD_PATH "${CPP_DIR_ABS}/$<TARGET_FILE_NAME:${MODULE_NAME}>")
    set(PYI_PATH "${CPP_DIR_ABS}/${MODULE_NAME}.pyi")

    # 1. Copy the built .pyd to the source folder after build
    add_custom_command(TARGET ${MODULE_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
            $<TARGET_FILE:${MODULE_NAME}>
            "${COPIED_PYD_PATH}"
        COMMENT "Copying ${MODULE_NAME} .pyd to source directory"
    )

    # 2. Generate .pyi stub (using the absolute path to the directory for sys.path)
    # NOTE: stubgen still needs the relative path ('test') to import from CWD for the pyi generation,
    # but the copy command needs the ABSOLUTE path. Let's simplify the stubgen as well.
    add_custom_command(TARGET ${MODULE_NAME} POST_BUILD
        COMMAND ${Python_EXECUTABLE} -c 
            "import sys; sys.path.append('${CPP_DIR_ABS}'); from nanobind import stubgen; stubgen.main(['-m', '${MODULE_NAME}', '-o', '${PYI_PATH}'])"
        COMMENT "Generating .pyi stub for ${MODULE_NAME}"
    )
endfunction()

add_nanobind_module(Vector2C src/extro/shared/Vector2C.cpp)
add_nanobind_module(RGBAColorC src/extro/shared/RGBAColorC.cpp)
add_nanobind_module(CollisionMask src/extro/internal/systems/Collision/CollisionMask.cpp)
