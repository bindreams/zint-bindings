cmake_minimum_required(VERSION 3.25)
project(zint-bindings)

add_subdirectory(external/pybind11)

option(ZINT_USE_QT "Overwrite" OFF)
option(ZINT_SHARED "Overwrite" OFF)
option(ZINT_STATIC "Overwrite" ON)
option(ZINT_FRONTEND "Overwrite" OFF)
add_subdirectory(external/zint)

pybind11_add_module(zint_bindings src/main.cpp)
file(GLOB_RECURSE cxregex_HEADERS CONFIGURE_DEPENDS "src/*.hpp")
target_sources(zint_bindings INTERFACE FILE_SET HEADERS BASE_DIRS src FILES ${cxregex_HEADERS})

set_target_properties(zint_bindings PROPERTIES OUTPUT_NAME zint)
target_link_libraries(zint_bindings PRIVATE zint-static)
target_compile_features(zint_bindings PUBLIC cxx_std_23)

install(
	TARGETS zint_bindings
	LIBRARY DESTINATION bin
)

find_package(Python3 COMPONENTS Interpreter REQUIRED)
if (DEFINED ENV{ZINT_BINDINGS_OVERRIDE_PIP_SITE_PACKAGES})
	set(SITE_PACKAGE_ARG --prefix "$ENV{ZINT_BINDINGS_OVERRIDE_PIP_SITE_PACKAGES}")
	message(STATUS "Zint-bindings python packages were overridden to install to $ENV{ZINT_BINDINGS_OVERRIDE_PIP_SITE_PACKAGES}")
else()
	# Not defined and will expand to empty string
endif()

# generate-enums.py script =============================================================================================
execute_process(
	COMMAND pip --disable-pip-version-check
		install ${SITE_PACKAGE_ARG} -r "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-enums.requirements.txt"
	COMMAND_ERROR_IS_FATAL ANY
)

add_custom_target(_generate_enums_hpp
	COMMAND "${Python3_EXECUTABLE}" scripts/generate-enums.py
	DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-enums.py"
	BYPRODUCTS "${CMAKE_CURRENT_SOURCE_DIR}/src/generated/enums.hpp"
	COMMENT "Creating src/generated/enums.hpp"
	WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
	VERBATIM
)
add_dependencies(zint_bindings _generate_enums_hpp)

# Copy artifacts to the target directory when installing from setup.py =================================================
if (DEFINED ENV{ZINT_BINDINGS_TARGET_DIR})
	add_custom_command(TARGET zint_bindings POST_BUILD
		COMMAND ${CMAKE_COMMAND} -E make_directory "$ENV{ZINT_BINDINGS_TARGET_DIR}/zint"
		COMMAND ${CMAKE_COMMAND} -E copy -t "$ENV{ZINT_BINDINGS_TARGET_DIR}/zint"
			"$<TARGET_FILE:zint_bindings>"
			"${CMAKE_CURRENT_BINARY_DIR}/zlib1.dll"
			"${CMAKE_CURRENT_BINARY_DIR}/libpng16.dll"
	)
	message(STATUS "Zint-bindings set to output to $ENV{ZINT_BINDINGS_TARGET_DIR}")
endif()
# ======================================================================================================================
