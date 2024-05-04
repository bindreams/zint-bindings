cmake_minimum_required(VERSION 3.28)

include(scripts/cmake/bundled-vcpkg.cmake)
if(SKBUILD)
	set(PROJECT_VERSION "${SKBUILD_PROJECT_VERSION}")
else()
	# On manual builds set a placeholder version.
	set(PROJECT_VERSION "0.0.0")
endif()

project(zint VERSION ${PROJECT_VERSION} LANGUAGES CXX)
message(STATUS "Zint bindings: version ${PROJECT_VERSION}")

if(WIN32)
	if (NOT MSVC)
		message(FATAL_ERROR "Zint can only be compiled on Windows using the MSVC compiler.")
	endif()

	if(CMAKE_GENERATOR MATCHES "Visual Studio .*")
		message(FATAL_ERROR "Visual Studio generator is not supported.\nPlease install Ninja: https://ninja-build.org/ and set CMAKE_GENERATOR environment variable to \"Ninja\".")
	endif()
endif()

if(NOT SKBUILD)
	include(scripts/cmake/find-packages-from-python.cmake)
endif()

find_package(pybind11 CONFIG REQUIRED)
find_package(fmt CONFIG REQUIRED)

set(ZINT_USE_QT OFF CACHE BOOL "")
set(ZINT_SHARED OFF CACHE BOOL "")
set(ZINT_STATIC ON CACHE BOOL "")
set(ZINT_FRONTEND OFF CACHE BOOL "")
add_subdirectory(external/zint)
set_target_properties(zint-static PROPERTIES
	POSITION_INDEPENDENT_CODE ON
	MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>"
)

set(TARGET_NAME "zint_bindings")
pybind11_add_module(${TARGET_NAME} MODULE src/main.cpp)
file(GLOB_RECURSE ${TARGET_NAME}_HEADERS CONFIGURE_DEPENDS "src/*.hpp" "src/*.inc")
target_sources(${TARGET_NAME} PRIVATE FILE_SET HEADERS BASE_DIRS src FILES ${${TARGET_NAME}_HEADERS})
set_target_properties(${TARGET_NAME} PROPERTIES
	OUTPUT_NAME zint
	MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>"
)

target_link_libraries(${TARGET_NAME} PRIVATE zint-static fmt::fmt)
target_compile_features(${TARGET_NAME} PRIVATE cxx_std_20)
target_compile_definitions(${TARGET_NAME} PRIVATE BINDINGS_VERSION=${PROJECT_VERSION})

include(scripts/cmake/warnings.cmake)
target_compile_warnings(${TARGET_NAME} PRIVATE
	GNU all extra pedantic error
	MSVC 4 X
)

install(TARGETS ${TARGET_NAME} LIBRARY DESTINATION . COMPONENT ${TARGET_NAME})

# generate-enums.py script =============================================================================================
find_package(Python3 COMPONENTS Interpreter REQUIRED)
add_custom_target(_generate_enums_hpp
	COMMAND "${Python3_EXECUTABLE}" scripts/generate-enums.py
	DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-enums.py"
	BYPRODUCTS "${CMAKE_CURRENT_SOURCE_DIR}/src/generated/enums.inc"
	COMMENT "Generating generated/enums.inc"
	WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
	VERBATIM
)
add_dependencies(${TARGET_NAME} _generate_enums_hpp)


execute_process(
	COMMAND pip --disable-pip-version-check install
		-r "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-stub.requirements.txt"
	COMMAND_ERROR_IS_FATAL ANY
)
add_custom_command(TARGET ${TARGET_NAME} POST_BUILD
	COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-stub.py"
	MAIN_DEPENDENCY ${TARGET_NAME}
	BYPRODUCTS "${CMAKE_CURRENT_SOURCE_DIR}/zint-stubs"
	COMMENT "Generating stub file"
	VERBATIM
)

if(Python3_VERSION_MINOR STREQUAL 12)
	# Copy stubs into the source directory so they are visible in source control and PRs
	add_custom_command(TARGET ${TARGET_NAME} POST_BUILD
		COMMAND "${CMAKE_COMMAND}" -E copy_directory
			"${CMAKE_CURRENT_BINARY_DIR}/zint-stubs"
			"${CMAKE_CURRENT_SOURCE_DIR}/../zint-stubs"
		MAIN_DEPENDENCY ${TARGET_NAME}
		BYPRODUCTS "${CMAKE_CURRENT_SOURCE_DIR}/../zint-stubs"
		COMMENT "Updating reference stub file"
		VERBATIM
	)
endif()

install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/zint-stubs" DESTINATION . COMPONENT ${TARGET_NAME})
