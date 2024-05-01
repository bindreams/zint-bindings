# On manual builds, add python site-packages to package prefixes.

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
execute_process(
	COMMAND ${Python3_EXECUTABLE} -m site --user-site
	OUTPUT_VARIABLE Python3_USERSITELIB
	RESULT_VARIABLE EXIT_CODE
)

if (EXIT_CODE GREATER_EQUAL 2)
	message(FATAL_ERROR "Unknown error getting user site-packages.")
endif()

if (EXIT_CODE EQUAL 0)
	string(STRIP "${Python3_USERSITELIB}" Python3_USERSITELIB)
	list(APPEND CMAKE_PREFIX_PATH "${Python3_USERSITELIB}")
endif()

list(APPEND CMAKE_PREFIX_PATH "${Python3_SITELIB}")
message(STATUS "Appended ${Python3_SITELIB} and ${Python3_USERSITELIB} to the list of cmake prefixes")
