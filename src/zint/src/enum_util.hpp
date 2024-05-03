// This magic was borrowed from https://gist.github.com/anntzer/96f27c0b88634dbc61862d08bff46d10
//
// The ``P11X_DECLARE_ENUM`` macro and the ``p11x::bind_enums`` function
// bind enums to Python's ``enum.Enum`` or one of its subclasses
// (``enum.IntEnum``, ``enum.Flag``, ``enum.IntFlag``) -- unlike
// ``pybind11::enum_`` which uses an unrelated implementation.
//
// Use as follows:
//
// .. code-block:: c++
//
//    // Define module_name.NameOfPythonEnum as an enum.Enum subclass, with
//    // members PyNameA, PyNameB, etc.
//
//    // This must happen at the toplevel, not within a namespace.
//    P11X_DECLARE_ENUM(
//      "NameOfPythonEnum",
//      "enum.Enum",  // or "enum.IntEnum", etc.
//      {"PyNameA", CEnumMemberA}, {"PyNameB", CEnumMemberB}, ...
//    )
//
//    // This must be within PYBIND11_MODULE, in the same translation unit as
//    // P11X_DECLARE_ENUM.
//    PYBIND11_MODULE(module_name, m) {
//      p11x::bind_enums(m);
//    }
//
// The enum members passed to ``P11X_DECLARE_ENUM`` must be actual members of the
// enum class, not integers with the corresponding value -- their type is used to
// infer the C class used by the caster.

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

struct EnumInfo {
	py::object& type_caster_reference;  /// pybind11::detail::type_caster's reference to a created class
	std::string name;
	std::string py_base;
	std::string docstring;

	// Actual enum items. The numeric value is a py::object because python integers are signed and have no max size.
	std::vector<std::pair<std::string, py::object>> items = {};

	template<typename T>
	EnumInfo& add(std::string_view name, T value) {
		static_assert(std::is_enum_v<T> || std::is_integral_v<T>, "Can only add integral values");
		using underlying_type = std::conditional_t<std::is_enum_v<T>, std::underlying_type_t<T>, T>;

		items.emplace_back(name, py::cast(static_cast<underlying_type>(value)));
		return *this;
	}
};

std::vector<EnumInfo> enums;

void bind_enums(py::module mod) {
	py::object locate = py::module::import("pydoc").attr("locate");

	for (auto const& info : enums) {
		py::object base_enum = locate(info.py_base);
		py::object cls = base_enum(info.name, info.items, py::arg("module") = mod.attr("__name__"));

		info.type_caster_reference = cls;
		mod.attr(py::cast(info.name)) = cls;
	}
}

}  // namespace
}  // namespace p11x

#define P11X_CONCAT2(a, b) a##b
#define P11X_CONCAT(a, b) P11X_CONCAT2(a, b)

// Immediately converting the args to a vector outside of the lambda avoids
// name collisions.
#define P11X_DECLARE_ENUM(py_name, type, py_base_cls, docstring)                                                       \
	namespace pybind11::detail {                                                                                       \
	template<>                                                                                                         \
	struct type_caster<type> {                                                                                         \
		static_assert(std::is_enum_v<type>, "Supplied type is not an enum type");                                      \
                                                                                                                       \
		static inline pybind11::object cls;                                                                            \
		PYBIND11_TYPE_CASTER(type, _(py_name));                                                                        \
                                                                                                                       \
		bool load(handle src, bool) {                                                                                  \
			if (!pybind11::isinstance(src, cls)) return false;                                                         \
                                                                                                                       \
			PyObject* tmp = PyNumber_Index(src.attr("value").ptr());                                                   \
			if (!tmp) return false;                                                                                    \
                                                                                                                       \
			Py_ssize_t ival = 0;                                                                                       \
			using underlying_type = std::underlying_type_t<type>;                                                      \
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
			value = static_cast<type>(ival);                                                                           \
			return true;                                                                                               \
		}                                                                                                              \
                                                                                                                       \
		static handle cast(type obj, return_value_policy, handle) {                                                    \
			return cls(std::underlying_type_t<type>(obj)).inc_ref();                                                   \
		}                                                                                                              \
	};                                                                                                                 \
	}                                                                                                                  \
                                                                                                                       \
	p11x::EnumInfo& P11X_CONCAT(_p11x_enum_, __COUNTER__) =                                                            \
		p11x::enums.emplace_back(pybind11::detail::type_caster<type>::cls, py_name, py_base_cls, docstring)
