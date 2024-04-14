cmake_minimum_required(VERSION 3.25)
project(zint-bindings)

if (DEFINED ENV{ZINT_BINDINGS_TARGET_DIRECTORY})
	set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "$ENV{ZINT_BINDINGS_TARGET_DIRECTORY}")
	message(STATUS "Zint-bindings set to output to ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
endif()

add_subdirectory(external/pybind11)

#cmake_policy(SET CMP0077 NEW)
option(ZINT_USE_QT "Overwrite" OFF)
option(ZINT_SHARED "Overwrite" OFF)
option(ZINT_STATIC "Overwrite" ON)
add_subdirectory(external/zint)

add_subdirectory(external/fmt)

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
# execute_process(
# 	COMMAND "${Python3_EXECUTABLE}" -m pip --disable-pip-version-check install scripts/generate-enums.requirements.txt
# 	COMMAND_ERROR_IS_FATAL ANY
# )

add_custom_target(_generate_enums_hpp
	"${Python3_EXECUTABLE}" scripts/generate-enums.py > src/generated/enums.hpp
	DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-enums.py"
	BYPRODUCTS "${CMAKE_CURRENT_SOURCE_DIR}/src/generated/generate-enums.py"
	COMMENT "Creating src/generated/enums.hpp"
	WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
	VERBATIM
)
add_dependencies(zint_bindings _generate_enums_hpp)

# include(InstallRequiredSystemLibraries)
# install(IMPORTED_RUNTIME_ARTIFACTS zint-static RUNTIME_DEPENDENCY_SET zint-static_RUNTIME_DEPENDENCY_SET)
# set(system32_regex "^$ENV{SystemRoot}\\system32")
# string(REPLACE "\\" "[\\/\\\\]" system32_regex "${system32_regex}")
# install(RUNTIME_DEPENDENCY_SET zint-static_RUNTIME_DEPENDENCY_SET
# 	PRE_EXCLUDE_REGEXES "api-ms-.*" "python312.dll"
# 	POST_EXCLUDE_REGEXES "${system32_regex}"
# )
