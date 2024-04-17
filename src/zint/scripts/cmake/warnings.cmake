cmake_minimum_required(VERSION 3.14.0)
#[=======================================================================[.rst:
.. command:: target_compile_warnings
    Add warning options to a target.

    .. signature::
        target_compile_warnings(<target>
            <PRIVATE|PUBLIC|INTERFACE>
                [GNU [flags...]]
                [MSVC [flags...]]
            [<PRIVATE|PUBLIC|INTERFACE> ...]
        )

    The function accepts two unrelated sets of flags: one for GNU-style compiler
    frontends, such as GCC and clang, and the other for MSVC-style compiler
    frontends, such as MSVC itself and clang-cl.

    Each flag is written the same as you would write it on the command line,
    except without the "-W" or "/W" prefix. For example:
        - ``-Wall`` becomes ``all``;
        - ``-Wbool-conversions`` becomes ``bool-conversions``;
        - ``/W4`` becomes ``4``;
        - ``/WX`` becomes ``X``.
    The only exception to this rule is ``-pedantic``, which is written as ``pedantic``.

    Warnings that are not recognised (such as ``-Wtrampolines`` which is recognized by GCC but not by clang) are
    silently ignored.

#]=======================================================================]
function(target_compile_warnings TARGET)
    # Parse arguments --------------------------------------------------------------------------------------------------
    cmake_parse_arguments(ARGS "" "" "INTERFACE;PUBLIC;PRIVATE" ${ARGN})
    if (DEFINED ARGS_UNPARSED_ARGUMENTS)
        list(JOIN ARGS_UNPARSED_ARGUMENTS ", " ARGS_UNPARSED_ARGUMENTS_STRING)
        set(ERROR_MESSAGE "Unrecognized arguments: ${ARGS_UNPARSED_ARGUMENTS_STRING}.")

        cmake_parse_arguments(NESTED "" "" "GNU;MSVC" ${ARGS_UNPARSED_ARGUMENTS})
        if(NOT DEFINED NESTED_UNPARSED_ARGUMENTS)
            set(ERROR_MESSAGE "${ERROR_MESSAGE} Did you forget to specify INTERFACE/PUBLIC/PRIVATE?")
        endif()

        message(SEND_ERROR "${ERROR_MESSAGE}")
        return()
    endif()
    # ------------------------------------------------------------------------------------------------------------------

    _target_compile_warnings_for_visibility(${TARGET} INTERFACE "${ARGS_INTERFACE}")
    _target_compile_warnings_for_visibility(${TARGET} PUBLIC    "${ARGS_PUBLIC}")
    _target_compile_warnings_for_visibility(${TARGET} PRIVATE   "${ARGS_PRIVATE}")
endfunction()

# Add compiler warnings for a single visibility setting (internal).
function(_target_compile_warnings_for_visibility TARGET VISIBILITY)
    # Parse arguments --------------------------------------------------------------------------------------------------
    cmake_parse_arguments(ARGS "" "" "GNU;MSVC" ${ARGN})
    if (DEFINED ARGS_UNPARSED_ARGUMENTS)
        list(JOIN ARGS_UNPARSED_ARGUMENTS ", " ARGS_UNPARSED_ARGUMENTS_STRING)
        message(SEND_ERROR "Unrecognized ${VISIBILITY} arguments: ${ARGS_UNPARSED_ARGUMENTS_STRING}.")
        return()
    endif()
    # ------------------------------------------------------------------------------------------------------------------
    set(GNU_SPECIAL_FLAGS_pedantic "-pedantic")

    if (CMAKE_CXX_COMPILER_FRONTEND_VARIANT STREQUAL "GNU")
        foreach(FLAG IN LISTS ARGS_GNU)
            if (DEFINED GNU_SPECIAL_FLAGS_${FLAG})
                _target_try_add_option(${TARGET} ${VISIBILITY} "${GNU_SPECIAL_FLAGS_${FLAG}}")
            else()
                _target_try_add_option(${TARGET} ${VISIBILITY} "-W${FLAG}")
            endif()
        endforeach()
    elseif(CMAKE_CXX_COMPILER_FRONTEND_VARIANT STREQUAL "MSVC")
        foreach(FLAG IN LISTS ARGS_MSVC)
            _target_try_add_option(${TARGET} ${VISIBILITY} "/W${FLAG}")
        endforeach()
    endif()
endfunction()

# Add a compiler option, if recognized by the compiler (internal).
include(CheckCXXCompilerFlag)
function(_target_try_add_option TARGET VISIBILITY FLAG)
    check_cxx_compiler_flag("${FLAG}" FLAG_SUPPORTED)

    if(FLAG_SUPPORTED)
        target_compile_options(${TARGET} ${VISIBILITY} "${FLAG}")
    endif()
endfunction()
