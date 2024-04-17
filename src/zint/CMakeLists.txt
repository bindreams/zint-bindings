cmake_minimum_required(VERSION 3.26)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES CXX)

find_package(pybind11 CONFIG REQUIRED)

set(ZINT_USE_QT OFF CACHE BOOL "")
set(ZINT_SHARED OFF CACHE BOOL "")
set(ZINT_STATIC ON CACHE BOOL "")
set(ZINT_FRONTEND OFF CACHE BOOL "")
add_subdirectory(external/zint)

set(TARGET_NAME "zint_bindings")
pybind11_add_module(${TARGET_NAME} MODULE src/main.cpp)
file(GLOB_RECURSE ${TARGET_NAME}_HEADERS CONFIGURE_DEPENDS "src/*.hpp")
target_sources(${TARGET_NAME} PRIVATE FILE_SET HEADERS BASE_DIRS src FILES ${${TARGET_NAME}_HEADERS})

set_target_properties(${TARGET_NAME} PROPERTIES OUTPUT_NAME zint)
target_link_libraries(${TARGET_NAME} PRIVATE zint-static)
target_compile_features(${TARGET_NAME} PRIVATE cxx_std_23)
target_compile_definitions(${TARGET_NAME} PRIVATE BINDINGS_VERSION=${PROJECT_VERSION})

include(scripts/cmake/warnings.cmake)
target_compile_warnings(${TARGET_NAME} PRIVATE
	GNU all extra pedantic error
	MSVC 4 X
)

install(TARGETS ${TARGET_NAME} LIBRARY DESTINATION . COMPONENT ${TARGET_NAME})

# generate-enums.py script =============================================================================================
find_package(Python3 COMPONENTS Interpreter REQUIRED)
execute_process(
	COMMAND pip --disable-pip-version-check
		install -r "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-enums.requirements.txt"
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
add_dependencies(${TARGET_NAME} _generate_enums_hpp)


execute_process(
	COMMAND pip --disable-pip-version-check
		install -r "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-stub.requirements.txt"
	COMMAND_ERROR_IS_FATAL ANY
)
add_custom_command(TARGET ${TARGET_NAME} POST_BUILD
	COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-stub.py"
		--output-dir zint-stubs
		--exit-code
		zint
	COMMAND "${CMAKE_COMMAND}" -E rename
		"${CMAKE_CURRENT_BINARY_DIR}/zint-stubs/zint.pyi"
		"${CMAKE_CURRENT_BINARY_DIR}/zint-stubs/__init__.pyi"
	COMMENT "Generating stub file"
	VERBATIM
)
install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/zint-stubs" DESTINATION . COMPONENT ${TARGET_NAME})
