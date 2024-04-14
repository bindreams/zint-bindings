cmake_minimum_required(VERSION 3.26)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES CXX)

find_package(pybind11 CONFIG REQUIRED)

option(ZINT_USE_QT "Override" OFF)
option(ZINT_SHARED "Override" OFF)
option(ZINT_STATIC "Override" ON)
option(ZINT_FRONTEND "Override" OFF)
add_subdirectory(external/zint)

set(TARGET_NAME "zint_bindings")
pybind11_add_module(${TARGET_NAME} MODULE src/zint/main.cpp)
file(GLOB_RECURSE ${TARGET_NAME}_HEADERS CONFIGURE_DEPENDS "src/zint/*.hpp")
target_sources(${TARGET_NAME} PRIVATE FILE_SET HEADERS BASE_DIRS src FILES ${${TARGET_NAME}_HEADERS})

set_target_properties(${TARGET_NAME} PROPERTIES OUTPUT_NAME zint)
target_link_libraries(${TARGET_NAME} PRIVATE zint-static)
target_compile_features(${TARGET_NAME} PRIVATE cxx_std_23)
target_compile_definitions(${TARGET_NAME} PRIVATE BINDINGS_VERSION=${PROJECT_VERSION})

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
	BYPRODUCTS "${CMAKE_CURRENT_SOURCE_DIR}/src/zint/generated/enums.hpp"
	COMMENT "Creating src/zint/generated/enums.hpp"
	WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
	VERBATIM
)
add_dependencies(${TARGET_NAME} _generate_enums_hpp)
