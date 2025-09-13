#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <array>
#include <cstring>
#include <limits>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string_view>
#include <type_traits>

#include "enums.hpp"
#include "utility.hpp"

#include <fmt/core.h>

// Include zint last, so that its defines do not mess with enums
#include <zint.h>

namespace py = pybind11;

#define PACKAGE_NAME zint

template<typename Derived>
struct SafeNextMixin {
	Derived* get_next() {
		auto& self = *static_cast<Derived*>(this);
		static_assert(SafelyReinterpretable<std::remove_cvref_t<decltype(*self.next)>, Derived>);

		return reinterpret_cast<Derived*>(self.next);
	}
};

struct VectorRect : public zint_vector_rect, SafeNextMixin<VectorRect> {};
struct VectorHexagon : public zint_vector_hexagon, SafeNextMixin<VectorHexagon> {};
struct VectorString : public zint_vector_string, SafeNextMixin<VectorString> {
	std::string_view get_text() { return reinterpret_cast<char*>(text); }
};

struct VectorCircle : public zint_vector_circle, SafeNextMixin<VectorCircle> {};

/// Wrapper around the linked-list structure of Vector* zint classes.
/// Instances of this are returned from Symbol instead of the first polygon with a pointer to the next.
template<typename T>
struct VectorList {
	T* m_head = nullptr;

	// For convenience, the class wants to provide __len__. Since this is a linked list, the size is calculated
	// on demand.
	static constexpr std::size_t UnknownSize = static_cast<std::size_t>(-1);
	std::size_t m_size = UnknownSize;

	struct iterator {
		T* m_item = nullptr;

		T& operator*() const { return *m_item; }
		iterator& operator++() {
			m_item = m_item->get_next();
			return *this;
		}

		friend bool operator==(iterator lhs, iterator rhs) { return lhs.m_item == rhs.m_item; }
		friend bool operator!=(iterator lhs, iterator rhs) { return !(lhs == rhs); }
	};

	auto begin() const { return iterator{m_head}; }
	auto end() const { return iterator{nullptr}; }

	std::size_t size() {
		if (m_size == UnknownSize) {
			m_size = 0;
			for (auto it = begin(); it != end(); ++it) ++m_size;
		}

		return m_size;
	}
};

using VectorRects = VectorList<VectorRect>;
using VectorHexagons = VectorList<VectorHexagon>;
using VectorStrings = VectorList<VectorString>;
using VectorCircles = VectorList<VectorCircle>;

struct Vector : public zint_vector {
	auto get_rectangles() { return VectorRects{access_as<VectorRect>(rectangles)}; }
	auto get_hexagons() { return VectorHexagons{access_as<VectorHexagon>(hexagons)}; }
	auto get_strings() { return VectorStrings{access_as<VectorString>(strings)}; }
	auto get_circles() { return VectorCircles{access_as<VectorCircle>(circles)}; }

private:
	template<typename T, typename U>
		requires SafelyReinterpretable<U, T>
	T* access_as(U* ptr) {
		return reinterpret_cast<T*>(ptr);
	}
};

struct Seg : public zint_seg {
public:
	Seg() : zint_seg{.source = nullptr, .length = 0, .eci = 0} {}
	Seg(py::buffer const& source, int eci) : zint_seg{} {
		set_source(source);
		this->eci = eci;
	}

	Seg(Seg const& other)
		: zint_seg{.source = new unsigned char[other.length], .length = other.length, .eci = other.eci} {
		std::memcpy(source, other.source, length);
	}
	Seg(Seg&& other) { swap(*this, other); }
	~Seg() {
		if (source != nullptr) delete[] source;
	}

	py::memoryview get_source() { return to_memoryview<1>(source, {length}, false); }
	void set_source(py::buffer const& val) {
		auto [data, size] = copy_buffer(val);
		if (size > std::numeric_limits<decltype(zint_seg::length)>::max()) throw py::value_error("buffer is too large");

		if (source != nullptr) delete[] source;
		source = data.release();
		length = static_cast<decltype(zint_seg::length)>(size);
	}

	friend void swap(Seg& lhs, Seg& rhs) {
		using std::swap;

		swap(lhs.source, rhs.source);
		swap(lhs.length, rhs.length);
		swap(lhs.eci, rhs.eci);
	}
};

struct StructApp : public zint_structapp {
	StructApp() : zint_structapp{.index = 0, .count = 0, .id = {}} {}
	StructApp(int index, int count, py::bytes const& id = {})
		: zint_structapp{.index = index, .count = count, .id = {}} {
		set_id(id);
	}

	py::bytes get_id() { return std::string_view(id, strnlen(id, std::extent_v<decltype(id)>)); }
	void set_id(py::bytes const& val) {
		std::string_view x{val};
		if (x.size() > 32) throw py::value_error(fmt::format("id size cannot be larger than 32, got {}", x.size()));

		std::memcpy(id, x.data(), x.size());
		if (x.size() < 32) id[x.size()] = '\0';
	}
};

struct Symbol {
	Symbol() : m_handle(ZBarcode_Create()) {}
	~Symbol() { ZBarcode_Delete(m_handle); }

	void clear() { ZBarcode_Clear(m_handle); }
	void reset() { ZBarcode_Reset(m_handle); }

	void encode(py::bytes const& data) {
		auto data_ = view_bytes(data);
		if (data_.size() > std::numeric_limits<int>::max()) throw py::value_error("buffer is too large");

		handle_error(ZBarcode_Encode(m_handle, data_.data(), static_cast<int>(data_.size())));
	}

	void encode(std::string_view text) {
		if (text.size() > std::numeric_limits<int>::max()) throw py::value_error("text is too long");

		handle_error(ZBarcode_Encode(
			m_handle, reinterpret_cast<unsigned char const*>(text.data()), static_cast<int>(text.size())
		));
	}

	void encode_segs(std::vector<Seg> const& segs) {
		static_assert(SafelyReinterpretable<Seg, zint_seg>);
		if (segs.size() > std::numeric_limits<int>::max()) throw py::value_error("too many segments");

		handle_error(
			ZBarcode_Encode_Segs(m_handle, static_cast<zint_seg const*>(segs.data()), static_cast<int>(segs.size()))
		);
	}

	void encode_segs(py::iterable const& segs) {
		std::vector<Seg> temp;

		for (auto iter = py::iter(segs); iter != iter.sentinel(); ++iter) {
			temp.push_back(*iter->cast<Seg*>());
		}

		encode_segs(temp);
	}

	void encode_file(const char* filename) { handle_error(ZBarcode_Encode_File(m_handle, filename)); }

	void print(int rotate_deg = 0) { handle_error(ZBarcode_Print(m_handle, rotate_deg)); }
	void buffer(int rotate_deg = 0) { handle_error(ZBarcode_Buffer(m_handle, rotate_deg)); }
	void buffer_vector(int rotate_deg = 0) { handle_error(ZBarcode_Buffer_Vector(m_handle, rotate_deg)); }

	// Static methods ==================================================================================================
	static CapabilityFlags capabilities(Symbology symbology) {
		// Send all 1 bits to ZBarcode_Cap which results in a return value of all supported flags xored together.
		return static_cast<CapabilityFlags>(
			ZBarcode_Cap(static_cast<int>(symbology), std::numeric_limits<unsigned int>::max())
		);
	}

	static float default_xdim(Symbology symbology) { return ZBarcode_Default_Xdim(static_cast<int>(symbology)); }
	static float scale_from_xdim_dp(
		Symbology symbology,
		float x_dim_mm,
		float dpmm,
		std::optional<const char*> filetype = std::nullopt
	) {
		// Note: `filetype` parameters are defined like this so that the type annotation stub generates with the correct
		// type annotation: `filetype: str | None`
		return ZBarcode_Scale_From_XdimDp(static_cast<int>(symbology), x_dim_mm, dpmm, filetype.value_or(nullptr));
	}

	static float xdim_dp_from_scale(
		Symbology symbology,
		float scale,
		float x_dim_mm_or_dpmm,
		std::optional<const char*> filetype = std::nullopt
	) {
		return ZBarcode_Scale_From_XdimDp(
			static_cast<int>(symbology), scale, x_dim_mm_or_dpmm, filetype.value_or(nullptr)
		);
	}

	// Member variables ================================================================================================
	void set_symbology(Symbology val) { m_handle->symbology = static_cast<int>(val); }
	Symbology get_symbology() { return static_cast<Symbology>(m_handle->symbology); }

	void set_height(float val) { m_handle->height = val; }
	float get_height() { return m_handle->height; }

	void set_scale(float val) { m_handle->scale = val; }
	float get_scale() { return m_handle->scale; }

	void set_whitespace_width(int val) { m_handle->whitespace_width = val; }
	int get_whitespace_width() { return m_handle->whitespace_width; }

	void set_whitespace_height(int val) { m_handle->whitespace_height = val; }
	int get_whitespace_height() { return m_handle->whitespace_height; }

	void set_border_width(int val) { m_handle->border_width = val; }
	int get_border_width() { return m_handle->border_width; }

	void set_output_options(OutputOptions val) { m_handle->output_options = static_cast<int>(val); }
	OutputOptions get_output_options() { return static_cast<OutputOptions>(m_handle->output_options); }

	void set_fgcolour(std::string_view val) {
		static constexpr int size = std::extent_v<decltype(m_handle->fgcolour)>;
		if (val.size() > size - 1)
			throw py::value_error(fmt::format("fgcolor string cannot be longer than {} characters", size - 1));

		memcpy(m_handle->fgcolour, val.data(), val.size());
		m_handle->fgcolour[val.size()] = '\0';
	}
	std::string_view get_fgcolour() { return m_handle->fgcolour; }

	void set_bgcolour(std::string_view val) {
		static constexpr int size = std::extent_v<decltype(m_handle->bgcolour)>;
		if (val.size() > size - 1)
			throw py::value_error(fmt::format("bgcolor string cannot be longer than {} characters", size - 1));

		memcpy(m_handle->bgcolour, val.data(), val.size());
		m_handle->bgcolour[val.size()] = '\0';
	}
	std::string_view get_bgcolour() { return m_handle->bgcolour; }

	void set_outfile(std::string_view val) {
		static constexpr int size = std::extent_v<decltype(m_handle->outfile)>;
		if (val.size() > size - 1)
			throw py::value_error(fmt::format("outfile cannot be longer than {} characters", size - 1));

		memcpy(m_handle->outfile, val.data(), val.size());
		m_handle->outfile[val.size()] = '\0';
	}
	std::string_view get_outfile() { return m_handle->outfile; }

	void set_primary(std::string_view val) {
		static constexpr int size = std::extent_v<decltype(m_handle->primary)>;
		if (val.size() > size - 1)
			throw py::value_error(fmt::format("primary cannot be longer than {} characters", size - 1));

		memcpy(m_handle->primary, val.data(), val.size());
		m_handle->primary[val.size()] = '\0';
	}
	std::string_view get_primary() { return m_handle->primary; }

	void set_option_1(int val) { m_handle->option_1 = val; }
	int get_option_1() { return m_handle->option_1; }

	void set_option_2(int val) { m_handle->option_2 = val; }
	int get_option_2() { return m_handle->option_2; }

	void set_option_3(int val) { m_handle->option_3 = val; }
	int get_option_3() { return m_handle->option_3; }

	void set_show_hrt(bool val) { m_handle->show_hrt = val; }
	bool get_show_hrt() { return m_handle->show_hrt; }

	void set_input_mode(InputMode val) { m_handle->input_mode = static_cast<int>(val); }
	InputMode get_input_mode() { return static_cast<InputMode>(m_handle->input_mode); }

	void set_eci(int val) { m_handle->eci = val; }
	int get_eci() { return m_handle->eci; }

	void set_dpmm(float val) { m_handle->dpmm = val; }
	float get_dpmm() { return m_handle->dpmm; }

	void set_dot_size(float val) { m_handle->dot_size = val; }
	float get_dot_size() { return m_handle->dot_size; }

	void set_text_gap(float val) { m_handle->text_gap = val; }
	float get_text_gap() { return m_handle->text_gap; }

	void set_guard_descent(float val) { m_handle->guard_descent = val; }
	float get_guard_descent() { return m_handle->guard_descent; }

	void set_structapp(StructApp val) { m_handle->structapp = val; }
	StructApp& get_structapp() {
		static_assert(SafelyReinterpretable<zint_structapp, StructApp>);

		return reinterpret_cast<StructApp&>(m_handle->structapp);
	}

	void set_warn_level(WarningLevel val) { m_handle->warn_level = static_cast<int>(val); }
	WarningLevel get_warn_level() { return static_cast<WarningLevel>(m_handle->warn_level); }

	void set_debug(int val) { m_handle->debug = val; }
	int get_debug() { return m_handle->debug; }

	std::string_view get_text() {
		return {
			reinterpret_cast<char*>(m_handle->text),
			static_cast<std::size_t>(m_handle->text_length),
		};
	}

	int get_rows() { return m_handle->rows; }

	int get_width() { return m_handle->width; }

	py::memoryview get_encoded_data() { return to_memoryview(m_handle->encoded_data, false); }

	py::list get_row_height() { return py::cast(m_handle->row_height); }

	std::string_view get_errtxt() { return m_handle->errtxt; }

	std::optional<py::memoryview> get_bitmap() {
		if (m_handle->bitmap == nullptr) return std::nullopt;

		return to_memoryview<3>(m_handle->bitmap, {m_handle->bitmap_height, m_handle->bitmap_width, 3}, true);
	}

	std::optional<py::memoryview> get_alphamap() {
		if (m_handle->alphamap == nullptr) return std::nullopt;

		return to_memoryview<2>(m_handle->alphamap, {m_handle->bitmap_height, m_handle->bitmap_width}, true);
	}

	Vector* get_vector() {
		static_assert(SafelyReinterpretable<zint_vector, Vector>);
		return reinterpret_cast<Vector*>(m_handle->vector);
	}

	std::optional<py::memoryview> get_memfile() {
		if (m_handle->memfile == nullptr) return std::nullopt;

		return to_memoryview<1>(m_handle->memfile, {m_handle->memfile_size}, true);
	}

private:
	void handle_error(int code) {
		if (code == 0) return;
		if (code < ZINT_ERROR) return issue_warning();

		switch (code) {
			case ZINT_ERROR_TOO_LONG:
			case ZINT_ERROR_INVALID_DATA:
			case ZINT_ERROR_INVALID_CHECK:
			case ZINT_ERROR_INVALID_OPTION:
			case ZINT_ERROR_ENCODING_PROBLEM:
			case ZINT_ERROR_FILE_ACCESS:
			case ZINT_ERROR_MEMORY:
			case ZINT_ERROR_FILE_WRITE:
			case ZINT_ERROR_USES_ECI:
			case ZINT_ERROR_NONCOMPLIANT:
			case ZINT_ERROR_HRT_TRUNCATED:
				throw std::runtime_error(m_handle->errtxt);
			default:
				throw std::runtime_error("unknown error");
		}
	}

	void issue_warning() {
		py::object logging = py::module_::import("logging");
		py::object getLogger = logging.attr("getLogger");
		py::object logger = getLogger(QUOTED(PACKAGE_NAME));
		py::object logger_warning = logger.attr("warning");

		std::string_view str = m_handle->errtxt;
		logger_warning(str);
	}

	zint_symbol* m_handle;
};

template<typename T>
void declare_vector_list(pybind11::module_& m, const char* python_identifier) {
	using list_t = VectorList<T>;

	py::class_<list_t>(m, python_identifier)
		.def("__len__", &list_t::size)
		.def(
			"__iter__",
			[](list_t const& obj) { return py::make_iterator(obj.begin(), obj.end()); },
			py::keep_alive<0, 1>()
		);
}

PYBIND11_MODULE(PACKAGE_NAME, m) {
	m.doc() = "A barcode encoding library supporting over 50 symbologies.";
	m.attr("__version__") = QUOTED(BINDINGS_VERSION);
	m.attr("__upstream_version__") = [] {
		// The implementation of ZBarcode_Version is kinda weird and this result will only make sense for release
		// versions of zint.
		int folded_version = ZBarcode_Version();
		return fmt::format(
			"{}.{}.{}", (folded_version / 10000) % 100, (folded_version / 100) % 100, folded_version % 100
		);
	}();

	p11x::bind_enums(m);

	// clang-format off
	py::class_<VectorRect>(m, "VectorRect")
		.def_readonly("x", &VectorRect::x, py::doc{"Left"})
		.def_readonly("y", &VectorRect::y, py::doc{"Top"})
		.def_readonly("width", &VectorRect::width)
		.def_readonly("height", &VectorRect::height)
		.def_readonly("colour", &VectorRect::colour, py::doc{"-1 for foreground, 1-8 for Cyan, Blue, Magenta, Red, Yellow, Green, Black, White"})
		.def_readonly("color", &VectorRect::colour, py::doc{"-1 for foreground, 1-8 for Cyan, Blue, Magenta, Red, Yellow, Green, Black, White. Alias of `colour`"})
		.doc() = "Rectangle vector elements returned from `Vector.rectangles`";

	py::class_<VectorHexagon>(m, "VectorHexagon")
		.def_readonly("x", &VectorHexagon::x, py::doc{"Centre"})
		.def_readonly("y", &VectorHexagon::y, py::doc{"Centre"})
		.def_readonly("diameter", &VectorHexagon::diameter, py::doc{"Short (minimal) diameter (i.e. diameter of inscribed circle)"})
		.def_readonly("rotation", &VectorHexagon::rotation, py::doc{"0, 90, 180, 270 degrees, where 0 has apex at top, i.e. short diameter is horizontal"})
		.doc() = "Hexagon vector elements returned from `Vector.hexagons`";

	py::class_<VectorString>(m, "VectorString")
		.def_readonly("x", &VectorString::x, py::doc{"Relative to halign (i.e. centre, left, right)"})
		.def_readonly("y", &VectorString::y, py::doc{"Relative to baseline"})
		.def_readonly("fsize", &VectorString::fsize, py::doc{"Font size"})
		.def_readonly("width", &VectorString::width, py::doc{"Rendered width estimate"})
		.def_readonly("length", &VectorString::length, py::doc{"Number of characters (bytes)"})
		.def_readonly("rotation", &VectorString::rotation, py::doc{"0, 90, 180, 270 degrees"})
		.def_readonly("halign", &VectorString::halign, py::doc{"Horizontal alignment: 0 for centre, 1 for left, 2 for right (end)"})
		.def_property_readonly("text", &VectorString::get_text)
		.doc() = "String vector elements returned from `Vector.strings`";

	py::class_<VectorCircle>(m, "VectorCircle")
		.def_readonly("x", &VectorCircle::x, py::doc{"Centre"})
		.def_readonly("y", &VectorCircle::y, py::doc{"Centre"})
		.def_readonly("diameter", &VectorCircle::diameter, py::doc{"Circle diameter. Does not include width (if any)"})
		.def_readonly("width", &VectorCircle::width, py::doc{"Width of circle perimeter (circumference). 0 for fill (disc)"})
		.def_readonly("colour", &VectorCircle::colour, py::doc{"Zero for draw with foreground colour (else draw with background colour (legacy))"})
		.def_readonly("color", &VectorCircle::colour, py::doc{"Zero for draw with foreground colour (else draw with background colour (legacy)). Alias of `colour`"})
		.doc() = "Circle vector elements returned from `Vector.circles`";

	declare_vector_list<VectorRect>(m, "VectorRects");
	declare_vector_list<VectorHexagon>(m, "VectorHexagons");
	declare_vector_list<VectorString>(m, "VectorStrings");
	declare_vector_list<VectorCircle>(m, "VectorCircles");

	py::class_<Vector>(m, "Vector")
		.def_readonly("width", &Vector::width, py::doc{"Width of barcode image (including text, whitespace)"})
		.def_readonly("height", &Vector::height, py::doc{"Height of barcode image (including text, whitespace)"})
		.def_property_readonly("rectangles", &Vector::get_rectangles, py::doc{"An iterable over rectangles (`VectorRectangle`)"})
		.def_property_readonly("hexagons", &Vector::get_hexagons, py::doc{"An iterable over hexagons (`VectorHexagon`)"})
		.def_property_readonly("strings", &Vector::get_strings, py::doc{"An iterable over strings (`VectorString`)"})
		.def_property_readonly("circles", &Vector::get_circles, py::doc{"An iterable over circles (`VectorCircle`)"})
		.doc() = "Vector image information, returned from `Symbol.vector` after calling `Symbol.buffer_vector`";

	py::class_<StructApp>(m, "StructApp")
		.def(py::init<>())
		.def(py::init<int, int, py::bytes const&>(), py::arg{"index"}, py::arg{"count"}, py::arg{"id"} = py::bytes{})
		.def_readwrite("index", &StructApp::index, py::doc{"Position in Structured Append sequence, 1-based. Must be <= `count`"})
		.def_readwrite("count", &StructApp::count, py::doc{"Number of symbols in Structured Append sequence. Set >= 2 to add SA Info"})
		.def_property("id", &StructApp::get_id, &StructApp::set_id, py::doc{"Optional ID to distinguish sequence, ASCII, max 32 long"})
		.doc() = "Structural append information (see `Symbol.structapp`).\n\nIgnored unless `StructApp.count` is non-zero";

	py::class_<Seg>(m, "Seg")
		.def(py::init<>())
		.def(py::init<py::buffer const&, int>())
		.def_property("source", &Seg::get_source, &Seg::set_source, py::doc{"Data to encode"})
		.def_readwrite("eci", &Seg::eci, py::doc{"Extended Channel Interpretation"})
		.doc() = "Segment for use with `Symbol.encode_segs`.";

	py::class_<Symbol>(m, "Symbol")
		.def(py::init<>())
		.def("clear", &Symbol::clear, py::doc{"Free any output buffers that may have been created and initialize output fields"})
		.def("reset", &Symbol::reset, py::doc{"Free any output buffers that may have been created and reset all fields to defaults"})
		.def("encode", py::overload_cast<py::bytes const&>(&Symbol::encode), py::arg{"data"}, py::doc{"Encode a barcode"})
		.def("encode", py::overload_cast<std::string_view>(&Symbol::encode), py::arg{"text"}, py::doc{"Encode a barcode"})
		.def("encode_segs", py::overload_cast<std::vector<Seg> const&>(&Symbol::encode_segs), py::arg{"segs"}, py::doc{"Encode a barcode with multiple ECI segments"})
		.def("encode_segs", py::overload_cast<py::iterable const&>(&Symbol::encode_segs), py::arg{"segs"}, py::doc{"Encode a barcode with multiple ECI segments"})
		.def("encode_file", &Symbol::encode_file, py::arg{"filename"}, py::pos_only{}, py::doc{"Encode a barcode using input data from file `filename`"})
		.def("print", &Symbol::print, py::arg{"rotate_deg"} = 0, py::doc{"Output a previously encoded symbol to file `Symbol.outfile`"})
		.def("buffer", &Symbol::buffer, py::arg{"rotate_deg"} = 0, py::doc{"Output a previously encoded symbol to memory as raster (`Symbol.bitmap`)"})
		.def("buffer_vector", &Symbol::buffer_vector, py::arg{"rotate_deg"} = 0, py::doc{"Output a previously encoded symbol to memory as vector (`Symbol.vector`)"})
		.def_static("capabilities", &Symbol::capabilities, py::arg{"symbology"}, py::pos_only{}, py::doc{"Return the capability flags for symbology `symbology`"})
		.def_static("default_xdim", &Symbol::default_xdim, py::arg{"symbology"}, py::pos_only{}, py::doc{"Return default X-dimension in mm for symbology `symbology`. Returns 0 on error (invalid `symbology`)"})
		.def_static("scale_from_xdim_dp", &Symbol::scale_from_xdim_dp, py::arg{"symbology"}, py::pos_only{}, py::arg{"x_dim_mm"}, py::kw_only{}, py::arg{"dpmm"}, py::arg{"filetype"} = py::none{}, py::doc{"Return the scale to use for `symbology` for non-zero X-dimension `x_dim_mm` at `dpmm` dots per mm for `filetype`. If `dpmm` zero defaults to 12. If `filetype` is None, defaults to \"GIF\". Returns 0 on error"})
		.def_static("xdim_dp_from_scale", &Symbol::xdim_dp_from_scale, py::arg{"symbology"},py::pos_only{},  py::arg{"scale"}, py::kw_only{}, py::arg{"x_dim_mm_or_dpmm"}, py::arg{"filetype"} = py::none{}, py::doc{"Reverse of `Symbol.scale_from_xdim_dp`. Estimate the X-dimension or dpmm given non-zero `scale` and non-zero `x_dim_mm_or_dpmm`. Return value bound to dpmm max not X-dimension max. Returns 0 on error"})
		.def_property("symbology", &Symbol::get_symbology, &Symbol::set_symbology, py::doc{"Symbol type to use (see `Symbology`)"})
		.def_property("height", &Symbol::get_height, &Symbol::set_height, py::doc{"Barcode height in X-dimensions (ignored for fixed-width barcodes)"})
		.def_property("scale", &Symbol::get_scale, &Symbol::set_scale, py::doc{"Scale factor when printing barcode, i.e. adjusts X-dimension. Default 1"})
		.def_property("whitespace_width", &Symbol::get_whitespace_width, &Symbol::set_whitespace_width, py::doc{"Width in X-dimensions of whitespace to left & right of barcode"})
		.def_property("whitespace_height", &Symbol::get_whitespace_height, &Symbol::set_whitespace_height, py::doc{"Height in X-dimensions of whitespace above & below the barcode"})
		.def_property("border_width", &Symbol::get_border_width, &Symbol::set_border_width, py::doc{"Size of border in X-dimensions"})
		.def_property("output_options", &Symbol::get_output_options, &Symbol::set_output_options, py::doc{"Various output parameters (bind, box etc, see `OutputOptions`)"})
		.def_property("fgcolour", &Symbol::get_fgcolour, &Symbol::set_fgcolour, py::doc{"Foreground as hexadecimal RGB/RGBA or decimal \"C,M,Y,K\" string"})
		.def_property("bgcolour", &Symbol::get_bgcolour, &Symbol::set_bgcolour, py::doc{"Background as hexadecimal RGB/RGBA or decimal \"C,M,Y,K\" string"})
		.def_property("fgcolor", &Symbol::get_fgcolour, &Symbol::set_fgcolour, py::doc{"Foreground as hexadecimal RGB/RGBA or decimal \"C,M,Y,K\" string. Alias of fgcolour."})
		.def_property("bgcolor", &Symbol::get_bgcolour, &Symbol::set_bgcolour, py::doc{"Background as hexadecimal RGB/RGBA or decimal \"C,M,Y,K\" string. Alias of bgcolour."})
		.def_property("outfile", &Symbol::get_outfile, &Symbol::set_outfile, py::doc{"Name of file to output to. Default \"out.png\""})
		.def_property("primary", &Symbol::get_primary, &Symbol::set_primary, py::doc{"Primary message data (MaxiCode, Composite)"})
		.def_property("option_1", &Symbol::get_option_1, &Symbol::set_option_1, py::doc{"Symbol-specific options"})
		.def_property("option_2", &Symbol::get_option_2, &Symbol::set_option_2, py::doc{"Symbol-specific options"})
		.def_property("option_3", &Symbol::get_option_3, &Symbol::set_option_3, py::doc{"Symbol-specific options"})
		.def_property("show_text", &Symbol::get_show_hrt, &Symbol::set_show_hrt, py::doc{"If `True`, display Human Readable Text (HRT) on supported barcodes. Default `True`"})
		.def_property("show_hrt", &Symbol::get_show_hrt, &Symbol::set_show_hrt, py::doc{"If `True`, display Human Readable Text (HRT) on supported barcodes. Default `True`. Alias of `Symbol.show_text`."})
		.def_property("input_mode", &Symbol::get_input_mode, &Symbol::set_input_mode, py::doc{"Encoding of input data (see `InputMode`). Default `InputMode.DATA`"})
		.def_property("eci", &Symbol::get_eci, &Symbol::set_eci, py::doc{"Extended Channel Interpretation. Default 0 (none)"})
		.def_property("dpmm", &Symbol::get_dpmm, &Symbol::set_dpmm, py::doc{"Resolution of output in dots per mm (BMP/EMF/PCX/PNG/TIF only). Default 0 (none)"})
		.def_property("dot_size", &Symbol::get_dot_size, &Symbol::set_dot_size, py::doc{"Size of dots used in BARCODE_DOTTY_MODE. Default 0.8"})
		.def_property("text_gap", &Symbol::get_text_gap, &Symbol::set_text_gap, py::doc{"Gap between barcode and Human Readable Text (HRT) in X-dimensions. Default 1"})
		.def_property("guard_descent", &Symbol::get_guard_descent, &Symbol::set_guard_descent, py::doc{"Height in X-dimensions that EAN/UPC guard bars descend. Default 5"})
		.def_property("structapp", &Symbol::get_structapp, &Symbol::set_structapp, py::doc{"Structured Append info. Default structapp.count 0 (none)"})
		.def_property("warn_level", &Symbol::get_warn_level, &Symbol::set_warn_level, py::doc{"Affects error/warning value returned by Zint API (see `WarningLevel`)"})
		.def_property("debug", &Symbol::get_debug, &Symbol::set_debug, py::doc{"Debugging flags"})
		.def_property_readonly("text", &Symbol::get_text, py::doc{"Human Readable Text (HRT) (if any), UTF-8 (output only)"})
		.def_property_readonly("rows", &Symbol::get_rows, py::doc{"Number of rows used by the symbol (output only)"})
		.def_property_readonly("width", &Symbol::get_width, py::doc{"Width of the generated symbol (output only)"})
		.def_property_readonly("encoded_data", &Symbol::get_encoded_data, py::doc{"Encoded data (output only). Allows for rows of 1152 modules"})
		.def_property_readonly("row_height", &Symbol::get_row_height, py::doc{"Heights of rows (output only). Allows for 200 row DotCode"})
		.def_property_readonly("errtxt", &Symbol::get_errtxt, py::doc{"Error message if an error or warning occurs (output only)"})
		.def_property_readonly("bitmap", &Symbol::get_bitmap, py::doc{"Stored bitmap image (raster output only)"})
		.def_property_readonly("alphamap", &Symbol::get_alphamap, py::doc{"Array of alpha values used (raster output only)"})
		.def_property_readonly("vector", &Symbol::get_vector, py::doc{"Vector header (vector output only)"})
		.def_property_readonly("memfile", &Symbol::get_memfile, py::doc{"In-memory file buffer if BARCODE_MEMORY_FILE (output only)"})
		.doc() = "Main symbol structure.";

	m.attr("__all__") = std::array{
		// The order will be reflected in the API documentation.
		// Main
		"Symbol",
		"Symbology",
		// Supporting classes
		"Seg",
		"StructApp",
		"Vector",
		"VectorCircle",
		"VectorHexagon",
		"VectorRect",
		"VectorString",
		// Enums
		"CapabilityFlags",
		"DataMatrixOptions",
		"InputMode",
		"OutputOptions",
		"QrFamilyOptions",
		"UltracodeOptions",
		"WarningLevel",
	};
	// clang-format on
}
