cmake_minimum_required(VERSION 3.28...4.1)

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
		message(FATAL_ERROR "Zint can only be compiled on Windows using the MSVC compiler. Please restart the command from a MSVC Developer shell.")
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

set(extension "zint_bindings")
pybind11_add_module(${extension} MODULE src/main.cpp)
file(GLOB_RECURSE ${extension}_HEADERS CONFIGURE_DEPENDS "src/*.hpp" "src/*.inc")
target_sources(${extension} PRIVATE FILE_SET HEADERS BASE_DIRS src FILES ${${extension}_HEADERS})
set_target_properties(${extension} PROPERTIES
	OUTPUT_NAME zint
	MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>"
)

target_link_libraries(${extension} PRIVATE zint-static fmt::fmt)
target_compile_features(${extension} PRIVATE cxx_std_20)
target_compile_definitions(${extension} PRIVATE BINDINGS_VERSION=${PROJECT_VERSION})

include(scripts/cmake/warnings.cmake)
target_compile_warnings(${extension} PRIVATE
	GNU all extra pedantic error
	MSVC 4 X
)

install(TARGETS ${extension} LIBRARY DESTINATION . COMPONENT ${extension})

# generate-enums.py ----------------------------------------------------------------------------------------------------
find_package(Python3 COMPONENTS Interpreter REQUIRED)
add_custom_target(_generate_enums
	COMMAND "${Python3_EXECUTABLE}" scripts/generate-enums.py
	DEPENDS "scripts/generate-enums.py"
	BYPRODUCTS "${CMAKE_CURRENT_SOURCE_DIR}/src/generated/enums.inc"
	WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
	COMMENT "Generating generated/enums.inc"
	VERBATIM
)
add_dependencies(${extension} _generate_enums)


# scripts/generate-stub.py ---------------------------------------------------------------------------------------------
execute_process(
	# Install dependencies at configure time
	COMMAND "${Python3_EXECUTABLE}" -m pip install -r "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-stub.requirements.txt"
	WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
	COMMAND_ERROR_IS_FATAL ANY
)
add_custom_command(TARGET ${extension} POST_BUILD
	COMMAND "${CMAKE_COMMAND}" -E make_directory "zint-stubs"
	COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate-stub.py"
		$<TARGET_FILE:${extension}>
		--format-config "${CMAKE_CURRENT_SOURCE_DIR}"
		--output "zint-stubs/__init__.pyi"
	BYPRODUCTS "${CMAKE_CURRENT_BUILD_DIR}/zint-stubs"
	WORKING_DIRECTORY "${CMAKE_CURRENT_BUILD_DIR}"
	COMMENT "Generating stub file"
	VERBATIM
)

if(Python3_VERSION_MINOR STREQUAL 13)  # Update this when Python 3.14 is released
	# Copy stubs into the source directory so they are visible in source control and PRs
	add_custom_command(TARGET ${extension} POST_BUILD
		COMMAND "${CMAKE_COMMAND}" -E copy
			"${CMAKE_CURRENT_BINARY_DIR}/zint-stubs/__init__.pyi"
			"src/generated/stubs.pyi"
		BYPRODUCTS "src/generated/stubs.pyi"
		WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
		COMMENT "Updating reference stub file"
		VERBATIM
	)
endif()

install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/zint-stubs" DESTINATION . COMPONENT ${extension})
# ----------------------------------------------------------------------------------------------------------------------
