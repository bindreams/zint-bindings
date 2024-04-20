# zint-bindings builds wheels with static linking and uses vcpkg for its dependencies.
# If CMAKE_TOOLCHAIN_FILE is not specified, this script will clone a known correct version of vcpkg and
# bootstrap it.

set(BUNDLED_VCPKG_PATH "${CMAKE_CURRENT_SOURCE_DIR}/.vcpkg")
set(BUNDLED_VCPKG_TOOLCHAIN "${BUNDLED_VCPKG_PATH}/scripts/buildsystems/vcpkg.cmake")

set(CMAKE_TOOLCHAIN_FILE "${BUNDLED_VCPKG_TOOLCHAIN}" CACHE STRING "Toolchain file")

if(CMAKE_TOOLCHAIN_FILE STREQUAL "${BUNDLED_VCPKG_TOOLCHAIN}")
	# If using our toolchain, clone vcpkg and run bootstrap on it
	if (NOT EXISTS "${BUNDLED_VCPKG_PATH}")
		find_program(GIT_EXECUTABLE git REQUIRED)
		execute_process(
			COMMAND "${GIT_EXECUTABLE}"
				clone https://github.com/microsoft/vcpkg
				--branch 2024.03.25
				"${BUNDLED_VCPKG_PATH}"
			COMMAND_ERROR_IS_FATAL ANY
		)
	endif()

	if (WIN32)
		set(BOOTSTRAP_SCRIPT "${BUNDLED_VCPKG_PATH}/bootstrap-vcpkg.bat")
		file(TO_NATIVE_PATH "${BOOTSTRAP_SCRIPT}" BOOTSTRAP_SCRIPT)
	else()
		set(BOOTSTRAP_SCRIPT "${BUNDLED_VCPKG_PATH}/bootstrap-vcpkg.sh")
	endif()

	execute_process(COMMAND "${BOOTSTRAP_SCRIPT}" COMMAND_ERROR_IS_FATAL ANY)
endif()

set(VCPKG_LIBRARY_LINKAGE "static" CACHE STRING "Vcpkg library linkage type")
