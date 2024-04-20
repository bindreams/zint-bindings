# On manual builds, add python site-packages to package prefixes.

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
execute_process(
	COMMAND ${Python3_EXECUTABLE} -m site --user-site
	OUTPUT_VARIABLE Python3_USERSITELIB
	COMMAND_ERROR_IS_FATAL ANY
)
string(STRIP "${Python3_USERSITELIB}" Python3_USERSITELIB)

message(STATUS "Appended ${Python3_SITELIB} and ${Python3_USERSITELIB} to the list of cmake prefixes")
list(APPEND CMAKE_PREFIX_PATH "${Python3_USERSITELIB}" "${Python3_SITELIB}")
