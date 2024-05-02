#pragma once
#define ENUM_BEGIN(name, type, _1, _2) enum class name : type {
#define ENUM_VALUE(_1, name, value, _2) name = value,
#define ENUM_END(_1)                                                                                                   \
	}                                                                                                                  \
	;

#include "generated/enums.inc"

#undef ENUM_BEGIN
#undef ENUM_VALUE
#undef ENUM_END

#include "generated/enum_declarations.hpp"
