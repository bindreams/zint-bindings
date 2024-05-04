/** Utilities for declaring native python enums with pybind11.
 *
 * Supports any python enum derived from `enum.Enum`. Inspired by
 * https://gist.github.com/anntzer/96f27c0b88634dbc61862d08bff46d10
 *
 * Usage example:
 * ```c++
 * enum class MyEnum {
 *     A = 0,
 *     B = 1,
 *     C = 1,
 *     D = 2
 * };
 *
 * P11X_DECLARE_ENUM("MyEnumPythonIdentifier", MyEnum, "enum.Enum", "My optional class docstring")
 *     .add("A", MyEnum::A, "Optional docstring")
 *     .add("B", MyEnum::B)
 *     .add("C", MyEnum::C)
 *     .add("D", MyEnum::D);
 *
 * // This must be within PYBIND11_MODULE, in the same translation unit as P11X_DECLARE_ENUM.
 * PYBIND11_MODULE(module_name, m) {
 *     p11x::bind_enums(m);
 * }
 *
 * ```
 */
#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <cstdint>
#include <string>
#include <string_view>
#include <type_traits>
#include <utility>
#include <vector>

namespace p11x {
namespace {
namespace py = pybind11;

/** Helper class holding info for a yet-unconstructed enum
 *
 * For constructing this, use the static method `Create`.
 */
struct EnumInfo {
	py::object& type_caster_reference;  /// pybind11::detail::type_caster's reference to a created class
	const bool needs_reinterpretation_as_unsigned;

	std::string name;
	std::string py_base;
	std::string docstring;

	// Actual enum items. The numeric value is a py::object because python integers are signed and have no max size.
	struct Value {
		using value_type = std::intmax_t;

		std::string name;
		value_type value;
		std::string docstring;
	};
	std::vector<Value> items = {};

	template<typename EnumType>
	static EnumInfo Create(std::string_view name, std::string_view py_base, std::string_view docstring = "") {
		using underlying_type = std::underlying_type_t<EnumType>;
		static_assert(
			sizeof(underlying_type) <= sizeof(Value::value_type), "Supplied enum's underlying type is too big"
		);

		return EnumInfo{
			.type_caster_reference = pybind11::detail::type_caster<EnumType>::cls,

			// if same size as holder type and unsigned (does not fit)
			.needs_reinterpretation_as_unsigned =
				std::is_unsigned_v<underlying_type> && sizeof(underlying_type) == sizeof(Value::value_type),
			.name = std::string{name},
			.py_base = std::string{py_base},
			.docstring = std::string{docstring}
		};
	}

	template<typename T>
	EnumInfo& add(std::string_view name, T value, std::string_view docstring = "") {
		static_assert(std::is_enum_v<T> || std::is_integral_v<T>, "Can only add integral values");

		items.push_back(Value{
			.name = std::string{name},
			.value = static_cast<Value::value_type>(value),
			.docstring = std::string{docstring}
		});
		return *this;
	}

	/// Get the items in an array suitable for constructing an `enum.Enum`.
	auto enum_ctor_items() const {
		std::vector<std::pair<std::string_view, py::object>> result;
		result.reserve(items.size());

		std::transform(items.begin(), items.end(), std::back_inserter(result), [&](auto& item) {
			py::object value;

			if (needs_reinterpretation_as_unsigned) {
				value = py::cast(static_cast<std::uintmax_t>(item.value));
			} else {
				value = py::cast(item.value);
			}

			return std::pair{std::string_view{item.name}, value};
		});

		return result;
	}
};

std::vector<EnumInfo> enums;

void bind_enums(py::module mod) {
	py::object locate = py::module::import("pydoc").attr("locate");

	for (auto const& info : enums) {
		py::object base_enum = locate(info.py_base);
		py::object cls = base_enum(info.name, info.enum_ctor_items(), py::arg("module") = mod.attr("__name__"));

		// Docstrings
		if (info.docstring != "") cls.doc() = info.docstring;
		for (auto& item : info.items) {
			if (item.docstring != "") cls.attr(item.name.c_str()).attr("__doc__") = item.docstring;
		}

		info.type_caster_reference = cls;
		mod.attr(info.name.c_str()) = cls;
	}
}

}  // namespace
}  // namespace p11x

#define P11X_CONCAT2(a, b) a##b
#define P11X_CONCAT(a, b) P11X_CONCAT2(a, b)

// Immediately converting the args to a vector outside of the lambda avoids
// name collisions.
#define P11X_DECLARE_ENUM(ENUM_NAME, ENUM_TYPE, PY_BASE, DOCSTRING)                                                    \
	namespace pybind11::detail {                                                                                       \
	template<>                                                                                                         \
	struct type_caster<ENUM_TYPE> {                                                                                    \
		static_assert(std::is_enum_v<ENUM_TYPE>, "Supplied type is not an enum type");                                 \
                                                                                                                       \
		static inline pybind11::object cls;                                                                            \
		PYBIND11_TYPE_CASTER(ENUM_TYPE, _(ENUM_NAME));                                                                 \
                                                                                                                       \
		bool load(handle src, bool) {                                                                                  \
			if (!pybind11::isinstance(src, cls)) return false;                                                         \
                                                                                                                       \
			PyObject* tmp = PyNumber_Index(src.attr("value").ptr());                                                   \
			if (!tmp) return false;                                                                                    \
                                                                                                                       \
			Py_ssize_t ival = 0;                                                                                       \
			using underlying_type = std::underlying_type_t<ENUM_TYPE>;                                                 \
			if constexpr (std::is_signed_v<underlying_type>) {                                                         \
				ival = PyLong_AsSsize_t(tmp);                                                                          \
			} else {                                                                                                   \
				/* This obviously might overflow, but since it's the same size and 2s compliment, it's okay. */        \
				/* The error value size_t(-1) also maps correctly to -1. */                                            \
				ival = static_cast<Py_ssize_t>(PyLong_AsSize_t(tmp));                                                  \
			}                                                                                                          \
                                                                                                                       \
			Py_DECREF(tmp);                                                                                            \
			if (ival == -1 && !PyErr_Occurred()) return false;                                                         \
                                                                                                                       \
			value = static_cast<ENUM_TYPE>(ival);                                                                      \
			return true;                                                                                               \
		}                                                                                                              \
                                                                                                                       \
		static handle cast(ENUM_TYPE obj, return_value_policy, handle) {                                               \
			return cls(std::underlying_type_t<ENUM_TYPE>(obj)).inc_ref();                                              \
		}                                                                                                              \
	};                                                                                                                 \
	}                                                                                                                  \
                                                                                                                       \
	p11x::EnumInfo& P11X_CONCAT(_p11x_enum_, __COUNTER__) =                                                            \
		p11x::enums.emplace_back(p11x::EnumInfo::Create<ENUM_TYPE>(ENUM_NAME, PY_BASE, DOCSTRING))
