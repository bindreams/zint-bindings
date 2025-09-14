#pragma once
#include <pybind11/pybind11.h>

#include <array>
#include <cstdint>
#include <span>
#include <string_view>
#include <type_traits>

#include <fmt/core.h>

namespace py = pybind11;

#define QUOTED_(...) #__VA_ARGS__
#define QUOTED(...) QUOTED_(__VA_ARGS__)

/**
 * @brief Returns true if `T` is an array bounded in all dimensions, such as x[10][20][30].
 *
 * Returns false for non-arrays, arrays with an unbounded dimension, and invalid arrays such as the following:
 * ```c++
 * int x[][10] = {};
 * ```
 *
 * The array above has the highest dimension deduced from initialization, but the initializer list is empty and the size
 * is deduced to 0, which is not allowed per C++ rules.
 */
template<typename T>
inline constexpr bool is_fully_bounded() {
	if constexpr (std::rank_v<T> == 0) return false;  // Not a valid array
	// For example, this condition is true for arrays like int x[][10] = {}, where first extent is deduced to 0.

	if constexpr (!std::is_bounded_array_v<T>) return false;
	if constexpr (std::rank_v<T> > 1) return is_fully_bounded<std::remove_extent_t<T>>();
	return true;
}

/// Concept that encapsulates the behavior of `is_fully_bounded`.
template<typename T>
concept BoundedNDArray = is_fully_bounded<T>();

template<BoundedNDArray T, std::size_t I = std::rank_v<T> - 1>
inline constexpr std::array<int, std::rank_v<T>> array_shape_impl() {
	if constexpr (I != 0) {
		auto result = array_shape_impl<T, I - 1>();
		result[I] = std::extent_v<T, I>;
		return result;
	} else {
		std::array<int, std::rank_v<T>> result{};
		result[I] = std::extent_v<T, I>;
		return result;
	}
}

/// An std::array containing the extents of a bounded N-dimensional array in order.
template<BoundedNDArray T>
inline constexpr std::array<int, std::rank_v<T>> array_shape = array_shape_impl<T>();

template<typename SourceT, typename TargetT>
concept SafelyReinterpretable =
	(std::is_base_of_v<SourceT, TargetT> || std::is_base_of_v<TargetT, SourceT>) && sizeof(SourceT) == sizeof(TargetT);

// Converter functions =================================================================================================

/// Convert a pointer to data and a shape to an N-dimensional pybind11 memory view.
template<std::size_t N, typename T>
inline py::memoryview to_memoryview(T* data, std::array<int, N> shape, bool readonly = false) {
	static_assert(sizeof(T) == 1, "memoryview only allows raw memory");
	std::array<int, N> strides;

	int stride = sizeof(T);
	for (int i = N - 1; i >= 0; i--) {
		strides[i] = stride;
		stride *= shape[i];
	}

	return py::memoryview::from_buffer(data, std::move(shape), std::move(strides), readonly);
}

/// Convert a C-style N-dimensional array into a memory view with the same shape.
template<BoundedNDArray T>
inline py::memoryview to_memoryview(T& data, bool readonly = false) {
	using value_type = std::remove_all_extents_t<T>;

	return to_memoryview<std::rank_v<T>>(reinterpret_cast<value_type*>(data), array_shape<T>, readonly);
}

/// Convert a C-style N-dimensional array into a numpy.ndarray with the same shape.
// Disabled because of a dependency on NumPy.
// template<BoundedNDArray T>
// inline auto to_ndarray(T& data) {
// 	using value_type = std::remove_all_extents_t<T>;
// 	return py::array_t<value_type>{array_shape<T>, reinterpret_cast<value_type*>(data)};
// }

/// Given a python bytes object, return a span over its contents.
inline std::span<unsigned char const> view_bytes(py::bytes const& bytes) {
	std::string_view x{bytes};
	return {reinterpret_cast<unsigned char const*>(x.data()), x.size()};
}

/// Copy a python buffer object of bytes and return a pointer and length.
[[nodiscard]] std::pair<std::unique_ptr<unsigned char[]>, std::size_t> copy_buffer(py::buffer const& data) {
	py::buffer_info info = data.request();

	if (info.ndim != 1) throw py::value_error(fmt::format("expected 1-dimensional data, got {} dimensions", info.ndim));
	if (info.itemsize != 1)
		throw py::value_error(fmt::format("expected a buffer of bytes, got an item size of {}", info.itemsize));

	auto result = std::make_unique<unsigned char[]>(info.size);
	if (info.size == 0) return {std::move(result), 0};

	if (info.strides[0] == 1) {
		// Objects are adjacent in memory
		std::memcpy(result.get(), info.ptr, info.size);
	} else {
		// Objects are adjacent in memory; copy them one-by-one.
		for (std::size_t i = 0; i < static_cast<std::size_t>(info.size); ++i) {
			result[i] = static_cast<unsigned char*>(info.ptr)[i * info.strides[0]];
		}
	}

	return {std::move(result), static_cast<size_t>(info.size)};
}
