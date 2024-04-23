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
				-c advice.detachedHead=false
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
		execute_process(COMMAND chmod +x "${BOOTSTRAP_SCRIPT}" COMMAND_ERROR_IS_FATAL ANY)
	endif()

	execute_process(COMMAND "${BOOTSTRAP_SCRIPT}" -disableMetrics COMMAND_ERROR_IS_FATAL ANY)
endif()

if(WIN32)
	# Windows is the only platform with dynamic linkage by default. Force static.
	if (DEFINED ENV{VCPKG_TARGET_TRIPLET})
		set(VCPKG_TARGET_TRIPLET "$ENV{VCPKG_TARGET_TRIPLET}")  # To print a message later
		unset(ENV{VCPKG_TARGET_TRIPLET})
	endif()

	if (DEFINED VCPKG_TARGET_TRIPLET)
		message(WARNING "Vcpkg target triplet has been redefined from \"${VCPKG_TARGET_TRIPLET}\" to \"x64-windows-static\"")
	endif()

	unset(VCPKG_TARGET_TRIPLET)
	unset(VCPKG_TARGET_TRIPLET CACHE)
	set(VCPKG_TARGET_TRIPLET "x64-windows-static" CACHE STRING "")
endif()
