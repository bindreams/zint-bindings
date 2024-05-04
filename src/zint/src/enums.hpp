#pragma once
#include "enum_util.hpp"

// Define actual C++ enums =============================================================================================
#define ENUM_BEGIN(enum_name, cpp_base, py_base, docstring) enum class enum_name : cpp_base {
#define ENUM_VALUE(enum_name, name, value, docstring) name = value,
#define ENUM_END(enum_name)                                                                                            \
	}                                                                                                                  \
	;

#include "generated/enums.inc"

#undef ENUM_BEGIN
#undef ENUM_VALUE
#undef ENUM_END

// Define python converters for these enums ============================================================================
// Call p11x::bind_enums(m); in module init!
#define ENUM_BEGIN(enum_name, cpp_base, py_base, docstring) P11X_DECLARE_ENUM(#enum_name, enum_name, py_base, docstring)
#define ENUM_VALUE(enum_name, name, value, docstring) .add(#name, enum_name::name, docstring)
#define ENUM_END(enum_name) ;

#include "generated/enums.inc"

#undef ENUM_BEGIN
#undef ENUM_VALUE
#undef ENUM_END
