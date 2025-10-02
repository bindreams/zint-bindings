# zint-bindings builds wheels with static linking and uses vcpkg for its dependencies.
# If CMAKE_TOOLCHAIN_FILE is not specified, this script will clone a known correct version of vcpkg and
# bootstrap it.

function(git_clone URL PATH REFERENCE)
	find_program(GIT_EXECUTABLE git REQUIRED)
	message(STATUS "Checking out ${URL}@${REFERENCE} into ${PATH}...")
	list(APPEND CMAKE_MESSAGE_INDENT "  ")

	# If path does not exist, do a fresh clone
	if (NOT EXISTS "${PATH}")
		message(STATUS "Cloning '${URL}'...")
		execute_process(
			COMMAND "${GIT_EXECUTABLE}" clone "${URL}" --no-checkout "${PATH}"
			COMMAND_ERROR_IS_FATAL ANY
		)
	endif()

	# Parse the reference
	execute_process(
		COMMAND "${GIT_EXECUTABLE}" rev-parse --verify "${REFERENCE}"
		WORKING_DIRECTORY "${PATH}"
		OUTPUT_VARIABLE commit_hash OUTPUT_STRIP_TRAILING_WHITESPACE
		RESULT_VARIABLE rev_parse_ok
		#COMMAND_ERROR_IS_FATAL  # not fatal
	)
	if (NOT "${rev_parse_ok}" EQUAL "0")  # If parse failed, fetch and retry
		message(STATUS "Fetching remotes...")
		execute_process(
			COMMAND "${GIT_EXECUTABLE}" fetch --all
			WORKING_DIRECTORY "${PATH}"
			COMMAND_ERROR_IS_FATAL ANY
		)
		execute_process(
			COMMAND "${GIT_EXECUTABLE}" rev-parse --verify "${REFERENCE}"
			WORKING_DIRECTORY "${PATH}"
			OUTPUT_VARIABLE commit_hash OUTPUT_STRIP_TRAILING_WHITESPACE
			COMMAND_ERROR_IS_FATAL ANY
		)
	endif()

	# Switch to the specified commit hash
	message(STATUS "Switching to ${commit_hash}...")
	execute_process(
		COMMAND "${GIT_EXECUTABLE}" -c advice.detachedHead=false switch --detach "${commit_hash}"
		WORKING_DIRECTORY "${PATH}"
		COMMAND_ERROR_IS_FATAL ANY
	)

	list(POP_BACK CMAKE_MESSAGE_INDENT)
	message(STATUS "Checking out ${URL}@${REFERENCE} into ${PATH}... done")
endfunction()

set(BUNDLED_VCPKG_PATH "${CMAKE_CURRENT_SOURCE_DIR}/.vcpkg")
set(BUNDLED_VCPKG_TOOLCHAIN "${BUNDLED_VCPKG_PATH}/scripts/buildsystems/vcpkg.cmake")

set(CMAKE_TOOLCHAIN_FILE "${BUNDLED_VCPKG_TOOLCHAIN}" CACHE STRING "Toolchain file")

if(CMAKE_TOOLCHAIN_FILE STREQUAL "${BUNDLED_VCPKG_TOOLCHAIN}")
	if (NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg.json")
		message(FATAL_ERROR "Could not find vcpkg.json in \"${CMAKE_CURRENT_SOURCE_DIR}\".\nbundled-vcpkg.cmake requires vcpkg.json with a specified version.")
	endif()

	file(READ "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg.json" VCPKG_JSON)
	string(JSON BUNDLED_VCPKG_SHA GET "${VCPKG_JSON}" "builtin-baseline")

	# If using our toolchain, clone vcpkg and run bootstrap on it
	git_clone("https://github.com/microsoft/vcpkg" "${BUNDLED_VCPKG_PATH}" "${BUNDLED_VCPKG_SHA}")

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

	if ("$ENV{PROCESSOR_ARCHITECTURE}" STREQUAL "AMD64")
		set(OVERRIDE_VCPKG_TARGET_TRIPLET "x64-windows-static")
	elseif("$ENV{PROCESSOR_ARCHITECTURE}" STREQUAL "ARM64")
		set(OVERRIDE_VCPKG_TARGET_TRIPLET "arm64-windows-static")
	else()
		message(FATAL_ERROR "Unsupported architecture \"$ENV{PROCESSOR_ARCHITECTURE}\"")
	endif()

	if (DEFINED VCPKG_TARGET_TRIPLET AND NOT "${VCPKG_TARGET_TRIPLET}" STREQUAL "${OVERRIDE_VCPKG_TARGET_TRIPLET}")
		message(WARNING "Vcpkg target triplet has been redefined from \"${VCPKG_TARGET_TRIPLET}\" to \"${OVERRIDE_VCPKG_TARGET_TRIPLET}\"")
	endif()

	unset(VCPKG_TARGET_TRIPLET)
	unset(VCPKG_TARGET_TRIPLET CACHE)
	set(VCPKG_TARGET_TRIPLET "${OVERRIDE_VCPKG_TARGET_TRIPLET}" CACHE STRING "")
	unset(OVERRIDE_VCPKG_TARGET_TRIPLET)
endif()
