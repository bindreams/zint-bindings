cmake_minimum_required(VERSION 3.23.0)

function(target_package TARGET)
	include(CMakePackageConfigHelpers)

	install(
		TARGETS ${TARGET}
		EXPORT "${TARGET}-targets"
		LIBRARY DESTINATION lib
		ARCHIVE DESTINATION lib
		RUNTIME DESTINATION bin
		INCLUDES DESTINATION include
		FILE_SET HEADERS DESTINATION include
	)

	install(
		EXPORT "${TARGET}-targets"
		FILE "${TARGET}-targets.cmake"
		NAMESPACE "${TARGET}::"
		DESTINATION "lib/cmake/${TARGET}"
	)

	configure_package_config_file(
		"${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config-template.cmake.in"
		"${CMAKE_CURRENT_BINARY_DIR}/${TARGET}-config.cmake"
		INSTALL_DESTINATION "lib/cmake/${TARGET}"
	)

	write_basic_package_version_file(
		"${TARGET}-config-version.cmake"
		VERSION "${${TARGET}_VERSION}"
		COMPATIBILITY SameMajorVersion
	)

	install(
		FILES
			"${CMAKE_CURRENT_BINARY_DIR}/${TARGET}-config.cmake"
			"${CMAKE_CURRENT_BINARY_DIR}/${TARGET}-config-version.cmake"
		DESTINATION "lib/cmake/${TARGET}"
	)
endfunction()
