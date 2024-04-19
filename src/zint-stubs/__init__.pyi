"""
A barcode encoding library supporting over 50 symbologies.
"""
from __future__ import annotations
import numpy
import typing
import typing_extensions
__all__ = ['CapabilityFlags', 'DataMatrixOptions', 'InputMode', 'OutputOptions', 'QrFamilyOptions', 'Seg', 'StructApp', 'Symbol', 'Symbology', 'UltracodeOptions', 'Vector', 'VectorCircle', 'VectorCircles', 'VectorHexagon', 'VectorHexagons', 'VectorRect', 'VectorRects', 'VectorString', 'VectorStrings', 'WarningLevel']
class CapabilityFlags:
    """
    Capability flags (ZBarcode_Cap() `cap_flag`)
    
    Members:
    
      HRT : Prints Human Readable Text?
    
      STACKABLE : Is stackable?
    
      EANUPC : Is EAN/UPC?
    
      EXTENDABLE : Legacy
    
      COMPOSITE : Can have composite data?
    
      ECI : Supports Extended Channel Interpretations?
    
      GS1 : Supports GS1 data?
    
      DOTTY : Can be output as dots?
    
      QUIET_ZONES : Has default quiet zones?
    
      FIXED_RATIO : Has fixed width-to-height (aspect) ratio?
    
      READER_INIT : Supports Reader Initialisation?
    
      FULL_MULTIBYTE : Supports full-multibyte option?
    
      MASK : Is mask selectable?
    
      STRUCTAPP : Supports Structured Append?
    
      COMPLIANT_HEIGHT : Has compliant height?
    """
    COMPLIANT_HEIGHT: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.COMPLIANT_HEIGHT: 8192>
    COMPOSITE: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.COMPOSITE: 8>
    DOTTY: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.DOTTY: 64>
    EANUPC: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.EANUPC: 4>
    ECI: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.ECI: 16>
    EXTENDABLE: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.EANUPC: 4>
    FIXED_RATIO: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.FIXED_RATIO: 256>
    FULL_MULTIBYTE: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.FULL_MULTIBYTE: 1024>
    GS1: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.GS1: 32>
    HRT: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.HRT: 1>
    MASK: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.MASK: 2048>
    QUIET_ZONES: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.QUIET_ZONES: 128>
    READER_INIT: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.READER_INIT: 512>
    STACKABLE: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.STACKABLE: 2>
    STRUCTAPP: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.STRUCTAPP: 4096>
    __members__: typing.ClassVar[dict[str, CapabilityFlags]]  # value = {'HRT': <CapabilityFlags.HRT: 1>, 'STACKABLE': <CapabilityFlags.STACKABLE: 2>, 'EANUPC': <CapabilityFlags.EANUPC: 4>, 'EXTENDABLE': <CapabilityFlags.EANUPC: 4>, 'COMPOSITE': <CapabilityFlags.COMPOSITE: 8>, 'ECI': <CapabilityFlags.ECI: 16>, 'GS1': <CapabilityFlags.GS1: 32>, 'DOTTY': <CapabilityFlags.DOTTY: 64>, 'QUIET_ZONES': <CapabilityFlags.QUIET_ZONES: 128>, 'FIXED_RATIO': <CapabilityFlags.FIXED_RATIO: 256>, 'READER_INIT': <CapabilityFlags.READER_INIT: 512>, 'FULL_MULTIBYTE': <CapabilityFlags.FULL_MULTIBYTE: 1024>, 'MASK': <CapabilityFlags.MASK: 2048>, 'STRUCTAPP': <CapabilityFlags.STRUCTAPP: 4096>, 'COMPLIANT_HEIGHT': <CapabilityFlags.COMPLIANT_HEIGHT: 8192>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class DataMatrixOptions:
    """
    Data Matrix specific options (`symbol->option_3`)
    
    Members:
    
      SQUARE : Only consider square versions on automatic symbol size selection
    
      DMRE : Consider DMRE versions on automatic symbol size selection
    
      ISO_144 : Use ISO instead of "de facto" format for 144x144 (i.e. don't skew ECC)
    """
    DMRE: typing.ClassVar[DataMatrixOptions]  # value = <DataMatrixOptions.DMRE: 101>
    ISO_144: typing.ClassVar[DataMatrixOptions]  # value = <DataMatrixOptions.ISO_144: 128>
    SQUARE: typing.ClassVar[DataMatrixOptions]  # value = <DataMatrixOptions.SQUARE: 100>
    __members__: typing.ClassVar[dict[str, DataMatrixOptions]]  # value = {'SQUARE': <DataMatrixOptions.SQUARE: 100>, 'DMRE': <DataMatrixOptions.DMRE: 101>, 'ISO_144': <DataMatrixOptions.ISO_144: 128>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class InputMode:
    """
    Values for `Symbol.input_mode`
    
    Members:
    
      DATA : Binary
    
      UNICODE : UTF-8
    
      GS1 : GS1. The following may be OR-ed with above
    
      ESCAPE : Process escape sequences
    
      GS1PARENS : Process parentheses as GS1 AI delimiters (instead of square brackets)
    
      GS1NOCHECK : Do not check validity of GS1 data (except that printable ASCII only)
    
      HEIGHTPERROW : Interpret `height` as per-row rather than as overall height
    
      FAST : Use faster if less optimal encodation or other shortcuts if available. Note: affects DATAMATRIX, MICROPDF417, PDF417, QRCODE & UPNQR only
    
      EXTRA_ESCAPE : Process special symbology-specific escape sequences. Note: currently Code 128 only
    """
    DATA: typing.ClassVar[InputMode]  # value = <InputMode.DATA: 0>
    ESCAPE: typing.ClassVar[InputMode]  # value = <InputMode.ESCAPE: 8>
    EXTRA_ESCAPE: typing.ClassVar[InputMode]  # value = <InputMode.EXTRA_ESCAPE: 256>
    FAST: typing.ClassVar[InputMode]  # value = <InputMode.FAST: 128>
    GS1: typing.ClassVar[InputMode]  # value = <InputMode.GS1: 2>
    GS1NOCHECK: typing.ClassVar[InputMode]  # value = <InputMode.GS1NOCHECK: 32>
    GS1PARENS: typing.ClassVar[InputMode]  # value = <InputMode.GS1PARENS: 16>
    HEIGHTPERROW: typing.ClassVar[InputMode]  # value = <InputMode.HEIGHTPERROW: 64>
    UNICODE: typing.ClassVar[InputMode]  # value = <InputMode.UNICODE: 1>
    __members__: typing.ClassVar[dict[str, InputMode]]  # value = {'DATA': <InputMode.DATA: 0>, 'UNICODE': <InputMode.UNICODE: 1>, 'GS1': <InputMode.GS1: 2>, 'ESCAPE': <InputMode.ESCAPE: 8>, 'GS1PARENS': <InputMode.GS1PARENS: 16>, 'GS1NOCHECK': <InputMode.GS1NOCHECK: 32>, 'HEIGHTPERROW': <InputMode.HEIGHTPERROW: 64>, 'FAST': <InputMode.FAST: 128>, 'EXTRA_ESCAPE': <InputMode.EXTRA_ESCAPE: 256>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __ge__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __gt__(self, other: typing.Any) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __le__(self, other: typing.Any) -> bool:
        ...
    def __lt__(self, other: typing.Any) -> bool:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OutputOptions:
    """
    Values for `Symbol.output_options`
    
    Members:
    
      BARCODE_BIND_TOP : Boundary bar above the symbol only (not below), does not affect stacking. Note: value was once used by the legacy (never-used) BARCODE_NO_ASCII
    
      BARCODE_BIND : Boundary bars above & below the symbol and between stacked symbols
    
      BARCODE_BOX : Box around symbol
    
      BARCODE_STDOUT : Output to stdout
    
      READER_INIT : Reader Initialisation (Programming)
    
      SMALL_TEXT : Use smaller font
    
      BOLD_TEXT : Use bold font
    
      CMYK_COLOUR : CMYK colour space (Encapsulated PostScript and TIF)
    
      BARCODE_DOTTY_MODE : Plot a matrix symbol using dots rather than squares
    
      GS1_GS_SEPARATOR : Use GS instead of FNC1 as GS1 separator (Data Matrix)
    
      OUT_BUFFER_INTERMEDIATE : Return ASCII values in bitmap buffer (OUT_BUFFER only)
    
      BARCODE_QUIET_ZONES : Add compliant quiet zones (additional to any specified whitespace). Note: CODE16K, CODE49, CODABLOCKF, ITF14, EAN/UPC have default quiet zones
    
      BARCODE_NO_QUIET_ZONES : Disable quiet zones, notably those with defaults as listed above
    
      COMPLIANT_HEIGHT : Warn if height not compliant, or use standard height (if any) as default
    
      EANUPC_GUARD_WHITESPACE : Add quiet zone indicators ("<"/">") to HRT whitespace (EAN/UPC)
    
      EMBED_VECTOR_FONT : Embed font in vector output - currently only for SVG output
    """
    BARCODE_BIND: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_BIND: 2>
    BARCODE_BIND_TOP: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_BIND_TOP: 1>
    BARCODE_BOX: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_BOX: 4>
    BARCODE_DOTTY_MODE: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_DOTTY_MODE: 256>
    BARCODE_NO_QUIET_ZONES: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_NO_QUIET_ZONES: 4096>
    BARCODE_QUIET_ZONES: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_QUIET_ZONES: 2048>
    BARCODE_STDOUT: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_STDOUT: 8>
    BOLD_TEXT: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BOLD_TEXT: 64>
    CMYK_COLOUR: typing.ClassVar[OutputOptions]  # value = <OutputOptions.CMYK_COLOUR: 128>
    COMPLIANT_HEIGHT: typing.ClassVar[OutputOptions]  # value = <OutputOptions.COMPLIANT_HEIGHT: 8192>
    EANUPC_GUARD_WHITESPACE: typing.ClassVar[OutputOptions]  # value = <OutputOptions.EANUPC_GUARD_WHITESPACE: 16384>
    EMBED_VECTOR_FONT: typing.ClassVar[OutputOptions]  # value = <OutputOptions.EMBED_VECTOR_FONT: 32768>
    GS1_GS_SEPARATOR: typing.ClassVar[OutputOptions]  # value = <OutputOptions.GS1_GS_SEPARATOR: 512>
    OUT_BUFFER_INTERMEDIATE: typing.ClassVar[OutputOptions]  # value = <OutputOptions.OUT_BUFFER_INTERMEDIATE: 1024>
    READER_INIT: typing.ClassVar[OutputOptions]  # value = <OutputOptions.READER_INIT: 16>
    SMALL_TEXT: typing.ClassVar[OutputOptions]  # value = <OutputOptions.SMALL_TEXT: 32>
    __members__: typing.ClassVar[dict[str, OutputOptions]]  # value = {'BARCODE_BIND_TOP': <OutputOptions.BARCODE_BIND_TOP: 1>, 'BARCODE_BIND': <OutputOptions.BARCODE_BIND: 2>, 'BARCODE_BOX': <OutputOptions.BARCODE_BOX: 4>, 'BARCODE_STDOUT': <OutputOptions.BARCODE_STDOUT: 8>, 'READER_INIT': <OutputOptions.READER_INIT: 16>, 'SMALL_TEXT': <OutputOptions.SMALL_TEXT: 32>, 'BOLD_TEXT': <OutputOptions.BOLD_TEXT: 64>, 'CMYK_COLOUR': <OutputOptions.CMYK_COLOUR: 128>, 'BARCODE_DOTTY_MODE': <OutputOptions.BARCODE_DOTTY_MODE: 256>, 'GS1_GS_SEPARATOR': <OutputOptions.GS1_GS_SEPARATOR: 512>, 'OUT_BUFFER_INTERMEDIATE': <OutputOptions.OUT_BUFFER_INTERMEDIATE: 1024>, 'BARCODE_QUIET_ZONES': <OutputOptions.BARCODE_QUIET_ZONES: 2048>, 'BARCODE_NO_QUIET_ZONES': <OutputOptions.BARCODE_NO_QUIET_ZONES: 4096>, 'COMPLIANT_HEIGHT': <OutputOptions.COMPLIANT_HEIGHT: 8192>, 'EANUPC_GUARD_WHITESPACE': <OutputOptions.EANUPC_GUARD_WHITESPACE: 16384>, 'EMBED_VECTOR_FONT': <OutputOptions.EMBED_VECTOR_FONT: 32768>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __ge__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __gt__(self, other: typing.Any) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __le__(self, other: typing.Any) -> bool:
        ...
    def __lt__(self, other: typing.Any) -> bool:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class QrFamilyOptions:
    """
    QR, Han Xin, Grid Matrix specific options (`symbol->option_3`)
    
    Members:
    
      FULL_MULTIBYTE : Enable Kanji/Hanzi compression for Latin-1 & binary data
    """
    FULL_MULTIBYTE: typing.ClassVar[QrFamilyOptions]  # value = <QrFamilyOptions.FULL_MULTIBYTE: 200>
    __members__: typing.ClassVar[dict[str, QrFamilyOptions]]  # value = {'FULL_MULTIBYTE': <QrFamilyOptions.FULL_MULTIBYTE: 200>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Seg:
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing_extensions.Buffer, arg1: int) -> None:
        ...
    @property
    def eci(self) -> int:
        """
        Extended Channel Interpretation
        """
    @eci.setter
    def eci(self, arg0: int) -> None:
        ...
    @property
    def source(self) -> memoryview:
        """
        Data to encode
        """
    @source.setter
    def source(self, arg1: typing_extensions.Buffer) -> None:
        ...
class StructApp:
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, index: int, count: int, id: bytes = b'') -> None:
        ...
    @property
    def count(self) -> int:
        """
        Number of symbols in Structured Append sequence. Set >= 2 to add SA Info
        """
    @count.setter
    def count(self, arg0: int) -> None:
        ...
    @property
    def id(self) -> bytes:
        """
        Optional ID to distinguish sequence, ASCII, max 32 long
        """
    @id.setter
    def id(self, arg1: bytes) -> None:
        ...
    @property
    def index(self) -> int:
        """
        Position in Structured Append sequence, 1-based. Must be <= `count`
        """
    @index.setter
    def index(self, arg0: int) -> None:
        ...
class Symbol:
    @staticmethod
    def capabilities(symbology: Symbology) -> CapabilityFlags:
        """
        Return the capability flags for symbology `symbology`
        """
    @staticmethod
    def default_xdim(symbology: Symbology) -> float:
        """
        Return default X-dimension in mm for symbology `symbology`. Returns 0 on error (invalid `symbology`)
        """
    @staticmethod
    def scale_from_xdim_dp(symbology: Symbology, /, x_dim_mm: float, *, dpmm: float, filetype: str | None = None) -> float:
        """
        Return the scale to use for `symbology` for non-zero X-dimension `x_dim_mm` at `dpmm` dots per mm for `filetype`. If `dpmm` zero defaults to 12. If `filetype` is None, defaults to "GIF". Returns 0 on error
        """
    @staticmethod
    def xdim_dp_from_scale(symbology: Symbology, /, scale: float, *, x_dim_mm_or_dpmm: float, filetype: str | None = None) -> float:
        """
        Reverse of `Symbol.scale_from_xdim_dp`. Estimate the X-dimension or dpmm given non-zero `scale` and non-zero `x_dim_mm_or_dpmm`. Return value bound to dpmm max not X-dimension max. Returns 0 on error
        """
    def __init__(self) -> None:
        ...
    def buffer(self, rotate_deg: int = 0) -> None:
        """
        Output a previously encoded symbol to memory as raster (`Symbol.bitmap`)
        """
    def buffer_vector(self, rotate_deg: int = 0) -> None:
        """
        Output a previously encoded symbol to memory as vector (`Symbol.vector`)
        """
    def clear(self) -> None:
        """
        Free any output buffers that may have been created and initialize output fields
        """
    @typing.overload
    def encode(self, data: bytes) -> None:
        """
        Encode a barcode
        """
    @typing.overload
    def encode(self, text: str) -> None:
        """
        Encode a barcode
        """
    def encode_file(self, filename: str) -> None:
        """
        Encode a barcode using input data from file `filename`
        """
    @typing.overload
    def encode_segs(self, segs: list[Seg]) -> None:
        """
        Encode a barcode with multiple ECI segments
        """
    @typing.overload
    def encode_segs(self, segs: typing.Iterable) -> None:
        """
        Encode a barcode with multiple ECI segments
        """
    def print(self, rotate_deg: int = 0) -> None:
        """
        Output a previously encoded symbol to file `Symbol.outfile`
        """
    def reset(self) -> None:
        """
        Free any output buffers that may have been created and reset all fields to defaults
        """
    @property
    def alphamap(self) -> memoryview | None:
        """
        Array of alpha values used (raster output only)
        """
    @property
    def bgcolor(self) -> str:
        """
        Background as hexadecimal RGB/RGBA or decimal "C,M,Y,K" string. Alias of bgcolour.
        """
    @bgcolor.setter
    def bgcolor(self, arg1: str) -> None:
        ...
    @property
    def bgcolour(self) -> str:
        """
        Background as hexadecimal RGB/RGBA or decimal "C,M,Y,K" string
        """
    @bgcolour.setter
    def bgcolour(self, arg1: str) -> None:
        ...
    @property
    def bitmap(self) -> memoryview | None:
        """
        Stored bitmap image (raster output only)
        """
    @property
    def border_width(self) -> int:
        """
        Size of border in X-dimensions
        """
    @border_width.setter
    def border_width(self, arg1: int) -> None:
        ...
    @property
    def debug(self) -> int:
        """
        Debugging flags
        """
    @debug.setter
    def debug(self, arg1: int) -> None:
        ...
    @property
    def dot_size(self) -> float:
        """
        Size of dots used in BARCODE_DOTTY_MODE. Default 0.8
        """
    @dot_size.setter
    def dot_size(self, arg1: float) -> None:
        ...
    @property
    def dpmm(self) -> float:
        """
        Resolution of output in dots per mm (BMP/EMF/PCX/PNG/TIF only). Default 0 (none)
        """
    @dpmm.setter
    def dpmm(self, arg1: float) -> None:
        ...
    @property
    def eci(self) -> int:
        """
        Extended Channel Interpretation. Default 0 (none)
        """
    @eci.setter
    def eci(self, arg1: int) -> None:
        ...
    @property
    def encoded_data(self) -> memoryview:
        """
        Encoded data (output only). Allows for rows of 1152 modules
        """
    @property
    def errtxt(self) -> str:
        """
        Error message if an error or warning occurs (output only)
        """
    @property
    def fgcolor(self) -> str:
        """
        Foreground as hexadecimal RGB/RGBA or decimal "C,M,Y,K" string. Alias of fgcolour.
        """
    @fgcolor.setter
    def fgcolor(self, arg1: str) -> None:
        ...
    @property
    def fgcolour(self) -> str:
        """
        Foreground as hexadecimal RGB/RGBA or decimal "C,M,Y,K" string
        """
    @fgcolour.setter
    def fgcolour(self, arg1: str) -> None:
        ...
    @property
    def guard_descent(self) -> float:
        """
        Height in X-dimensions that EAN/UPC guard bars descend. Default 5
        """
    @guard_descent.setter
    def guard_descent(self, arg1: float) -> None:
        ...
    @property
    def height(self) -> float:
        """
        Barcode height in X-dimensions (ignored for fixed-width barcodes)
        """
    @height.setter
    def height(self, arg1: float) -> None:
        ...
    @property
    def input_mode(self) -> int:
        """
        Encoding of input data (see DATA_MODE etc below). Default DATA_MODE
        """
    @input_mode.setter
    def input_mode(self, arg1: int) -> None:
        ...
    @property
    def option_1(self) -> int:
        """
        Symbol-specific options
        """
    @option_1.setter
    def option_1(self, arg1: int) -> None:
        ...
    @property
    def option_2(self) -> int:
        """
        Symbol-specific options
        """
    @option_2.setter
    def option_2(self, arg1: int) -> None:
        ...
    @property
    def option_3(self) -> int:
        """
        Symbol-specific options
        """
    @option_3.setter
    def option_3(self, arg1: int) -> None:
        ...
    @property
    def outfile(self) -> str:
        """
        Name of file to output to. Default "out.png"
        """
    @outfile.setter
    def outfile(self, arg1: str) -> None:
        ...
    @property
    def output_options(self) -> int:
        """
        Various output parameters (bind, box etc, see below)
        """
    @output_options.setter
    def output_options(self, arg1: int) -> None:
        ...
    @property
    def primary(self) -> str:
        """
        Primary message data (MaxiCode, Composite)
        """
    @primary.setter
    def primary(self, arg1: str) -> None:
        ...
    @property
    def row_height(self) -> numpy.ndarray[typing.Any, numpy.dtype[numpy.float32]]:
        """
        Heights of rows (output only). Allows for 200 row DotCode
        """
    @property
    def rows(self) -> int:
        """
        Number of rows used by the symbol (output only)
        """
    @property
    def scale(self) -> float:
        """
        Scale factor when printing barcode, i.e. adjusts X-dimension. Default 1
        """
    @scale.setter
    def scale(self, arg1: float) -> None:
        ...
    @property
    def show_hrt(self) -> bool:
        """
        Show (1) or hide (0) Human Readable Text (HRT). Default 1
        """
    @show_hrt.setter
    def show_hrt(self, arg1: bool) -> None:
        ...
    @property
    def structapp(self) -> StructApp:
        """
        Structured Append info. Default structapp.count 0 (none)
        """
    @structapp.setter
    def structapp(self, arg1: StructApp) -> None:
        ...
    @property
    def symbology(self) -> Symbology:
        """
        Symbol to use (see BARCODE_XXX below)
        """
    @symbology.setter
    def symbology(self, arg1: Symbology) -> None:
        ...
    @property
    def text(self) -> str:
        """
        Human Readable Text (HRT) (if any), UTF-8 (output only)
        """
    @property
    def text_gap(self) -> float:
        """
        Gap between barcode and text (HRT) in X-dimensions. Default 1
        """
    @text_gap.setter
    def text_gap(self, arg1: float) -> None:
        ...
    @property
    def vector(self) -> Vector:
        """
        Vector header (vector output only)
        """
    @property
    def warn_level(self) -> int:
        """
        Affects error/warning value returned by Zint API (see WARN_XXX below)
        """
    @warn_level.setter
    def warn_level(self, arg1: int) -> None:
        ...
    @property
    def whitespace_height(self) -> int:
        """
        Height in X-dimensions of whitespace above & below the barcode
        """
    @whitespace_height.setter
    def whitespace_height(self, arg1: int) -> None:
        ...
    @property
    def whitespace_width(self) -> int:
        """
        Width in X-dimensions of whitespace to left & right of barcode
        """
    @whitespace_width.setter
    def whitespace_width(self, arg1: int) -> None:
        ...
    @property
    def width(self) -> int:
        """
        Width of the generated symbol (output only)
        """
class Symbology:
    """
    Values for `Symbol.symbology`
    
    Members:
    
      CODE11 : Code 11
    
      C25STANDARD : 2 of 5 Standard (Matrix)
    
      C25INTER : 2 of 5 Interleaved
    
      C25IATA : 2 of 5 IATA
    
      C25LOGIC : 2 of 5 Data Logic
    
      C25IND : 2 of 5 Industrial
    
      CODE39 : Code 39
    
      EXCODE39 : Extended Code 39
    
      EANX : EAN (European Article Number)
    
      EANX_CHK : EAN + Check Digit
    
      GS1_128 : GS1-128
    
      CODABAR : Codabar
    
      CODE128 : Code 128
    
      DPLEIT : Deutsche Post Leitcode
    
      DPIDENT : Deutsche Post Identcode
    
      CODE16K : Code 16k
    
      CODE49 : Code 49
    
      CODE93 : Code 93
    
      FLAT : Flattermarken
    
      DBAR_OMN : GS1 DataBar Omnidirectional
    
      DBAR_LTD : GS1 DataBar Limited
    
      DBAR_EXP : GS1 DataBar Expanded
    
      TELEPEN : Telepen Alpha
    
      UPCA : UPC-A
    
      UPCA_CHK : UPC-A + Check Digit
    
      UPCE : UPC-E
    
      UPCE_CHK : UPC-E + Check Digit
    
      POSTNET : USPS (U.S. Postal Service) POSTNET
    
      MSI_PLESSEY : MSI Plessey
    
      FIM : Facing Identification Mark
    
      LOGMARS : LOGMARS
    
      PHARMA : Pharmacode One-Track
    
      PZN : Pharmazentralnummer
    
      PHARMA_TWO : Pharmacode Two-Track
    
      CEPNET : Brazilian CEPNet Postal Code
    
      PDF417 : PDF417
    
      PDF417COMP : Compact PDF417 (Truncated PDF417)
    
      MAXICODE : MaxiCode
    
      QRCODE : QR Code
    
      CODE128AB : Code 128 (Suppress Code Set C)
    
      AUSPOST : Australia Post Standard Customer
    
      AUSREPLY : Australia Post Reply Paid
    
      AUSROUTE : Australia Post Routing
    
      AUSREDIRECT : Australia Post Redirection
    
      ISBNX : ISBN
    
      RM4SCC : Royal Mail 4-State Customer Code
    
      DATAMATRIX : Data Matrix (ECC200)
    
      EAN14 : EAN-14
    
      VIN : Vehicle Identification Number
    
      CODABLOCKF : Codablock-F
    
      NVE18 : NVE-18 (SSCC-18)
    
      JAPANPOST : Japanese Postal Code
    
      KOREAPOST : Korea Post
    
      DBAR_STK : GS1 DataBar Stacked
    
      DBAR_OMNSTK : GS1 DataBar Stacked Omnidirectional
    
      DBAR_EXPSTK : GS1 DataBar Expanded Stacked
    
      PLANET : USPS PLANET
    
      MICROPDF417 : MicroPDF417
    
      USPS_IMAIL : USPS Intelligent Mail (OneCode)
    
      PLESSEY : UK Plessey
    
      TELEPEN_NUM : Telepen Numeric
    
      ITF14 : ITF-14
    
      KIX : Dutch Post KIX Code
    
      AZTEC : Aztec Code
    
      DAFT : DAFT Code
    
      DPD : DPD Code
    
      MICROQR : Micro QR Code
    
      HIBC_128 : HIBC (Health Industry Barcode) Code 128
    
      HIBC_39 : HIBC Code 39
    
      HIBC_DM : HIBC Data Matrix
    
      HIBC_QR : HIBC QR Code
    
      HIBC_PDF : HIBC PDF417
    
      HIBC_MICPDF : HIBC MicroPDF417
    
      HIBC_BLOCKF : HIBC Codablock-F
    
      HIBC_AZTEC : HIBC Aztec Code
    
      DOTCODE : DotCode
    
      HANXIN : Han Xin (Chinese Sensible) Code
    
      MAILMARK_2D : Royal Mail 2D Mailmark (CMDM) (Data Matrix)
    
      UPU_S10 : Universal Postal Union S10
    
      MAILMARK_4S : Royal Mail 4-State Mailmark
    
      AZRUNE : Aztec Runes
    
      CODE32 : Code 32
    
      EANX_CC : EAN Composite
    
      GS1_128_CC : GS1-128 Composite
    
      DBAR_OMN_CC : GS1 DataBar Omnidirectional Composite
    
      DBAR_LTD_CC : GS1 DataBar Limited Composite
    
      DBAR_EXP_CC : GS1 DataBar Expanded Composite
    
      UPCA_CC : UPC-A Composite
    
      UPCE_CC : UPC-E Composite
    
      DBAR_STK_CC : GS1 DataBar Stacked Composite
    
      DBAR_OMNSTK_CC : GS1 DataBar Stacked Omnidirectional Composite
    
      DBAR_EXPSTK_CC : GS1 DataBar Expanded Stacked Composite
    
      CHANNEL : Channel Code
    
      CODEONE : Code One
    
      GRIDMATRIX : Grid Matrix
    
      UPNQR : UPNQR (Univerzalnega Plačilnega Naloga QR)
    
      ULTRA : Ultracode
    
      RMQR : Rectangular Micro QR Code (rMQR)
    
      BC412 : IBM BC412 (SEMI T1-95)
    """
    AUSPOST: typing.ClassVar[Symbology]  # value = <Symbology.AUSPOST: 63>
    AUSREDIRECT: typing.ClassVar[Symbology]  # value = <Symbology.AUSREDIRECT: 68>
    AUSREPLY: typing.ClassVar[Symbology]  # value = <Symbology.AUSREPLY: 66>
    AUSROUTE: typing.ClassVar[Symbology]  # value = <Symbology.AUSROUTE: 67>
    AZRUNE: typing.ClassVar[Symbology]  # value = <Symbology.AZRUNE: 128>
    AZTEC: typing.ClassVar[Symbology]  # value = <Symbology.AZTEC: 92>
    BC412: typing.ClassVar[Symbology]  # value = <Symbology.BC412: 146>
    C25IATA: typing.ClassVar[Symbology]  # value = <Symbology.C25IATA: 4>
    C25IND: typing.ClassVar[Symbology]  # value = <Symbology.C25IND: 7>
    C25INTER: typing.ClassVar[Symbology]  # value = <Symbology.C25INTER: 3>
    C25LOGIC: typing.ClassVar[Symbology]  # value = <Symbology.C25LOGIC: 6>
    C25STANDARD: typing.ClassVar[Symbology]  # value = <Symbology.C25STANDARD: 2>
    CEPNET: typing.ClassVar[Symbology]  # value = <Symbology.CEPNET: 54>
    CHANNEL: typing.ClassVar[Symbology]  # value = <Symbology.CHANNEL: 140>
    CODABAR: typing.ClassVar[Symbology]  # value = <Symbology.CODABAR: 18>
    CODABLOCKF: typing.ClassVar[Symbology]  # value = <Symbology.CODABLOCKF: 74>
    CODE11: typing.ClassVar[Symbology]  # value = <Symbology.CODE11: 1>
    CODE128: typing.ClassVar[Symbology]  # value = <Symbology.CODE128: 20>
    CODE128AB: typing.ClassVar[Symbology]  # value = <Symbology.CODE128AB: 60>
    CODE16K: typing.ClassVar[Symbology]  # value = <Symbology.CODE16K: 23>
    CODE32: typing.ClassVar[Symbology]  # value = <Symbology.CODE32: 129>
    CODE39: typing.ClassVar[Symbology]  # value = <Symbology.CODE39: 8>
    CODE49: typing.ClassVar[Symbology]  # value = <Symbology.CODE49: 24>
    CODE93: typing.ClassVar[Symbology]  # value = <Symbology.CODE93: 25>
    CODEONE: typing.ClassVar[Symbology]  # value = <Symbology.CODEONE: 141>
    DAFT: typing.ClassVar[Symbology]  # value = <Symbology.DAFT: 93>
    DATAMATRIX: typing.ClassVar[Symbology]  # value = <Symbology.DATAMATRIX: 71>
    DBAR_EXP: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_EXP: 31>
    DBAR_EXPSTK: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_EXPSTK: 81>
    DBAR_EXPSTK_CC: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_EXPSTK_CC: 139>
    DBAR_EXP_CC: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_EXP_CC: 134>
    DBAR_LTD: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_LTD: 30>
    DBAR_LTD_CC: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_LTD_CC: 133>
    DBAR_OMN: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_OMN: 29>
    DBAR_OMNSTK: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_OMNSTK: 80>
    DBAR_OMNSTK_CC: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_OMNSTK_CC: 138>
    DBAR_OMN_CC: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_OMN_CC: 132>
    DBAR_STK: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_STK: 79>
    DBAR_STK_CC: typing.ClassVar[Symbology]  # value = <Symbology.DBAR_STK_CC: 137>
    DOTCODE: typing.ClassVar[Symbology]  # value = <Symbology.DOTCODE: 115>
    DPD: typing.ClassVar[Symbology]  # value = <Symbology.DPD: 96>
    DPIDENT: typing.ClassVar[Symbology]  # value = <Symbology.DPIDENT: 22>
    DPLEIT: typing.ClassVar[Symbology]  # value = <Symbology.DPLEIT: 21>
    EAN14: typing.ClassVar[Symbology]  # value = <Symbology.EAN14: 72>
    EANX: typing.ClassVar[Symbology]  # value = <Symbology.EANX: 13>
    EANX_CC: typing.ClassVar[Symbology]  # value = <Symbology.EANX_CC: 130>
    EANX_CHK: typing.ClassVar[Symbology]  # value = <Symbology.EANX_CHK: 14>
    EXCODE39: typing.ClassVar[Symbology]  # value = <Symbology.EXCODE39: 9>
    FIM: typing.ClassVar[Symbology]  # value = <Symbology.FIM: 49>
    FLAT: typing.ClassVar[Symbology]  # value = <Symbology.FLAT: 28>
    GRIDMATRIX: typing.ClassVar[Symbology]  # value = <Symbology.GRIDMATRIX: 142>
    GS1_128: typing.ClassVar[Symbology]  # value = <Symbology.GS1_128: 16>
    GS1_128_CC: typing.ClassVar[Symbology]  # value = <Symbology.GS1_128_CC: 131>
    HANXIN: typing.ClassVar[Symbology]  # value = <Symbology.HANXIN: 116>
    HIBC_128: typing.ClassVar[Symbology]  # value = <Symbology.HIBC_128: 98>
    HIBC_39: typing.ClassVar[Symbology]  # value = <Symbology.HIBC_39: 99>
    HIBC_AZTEC: typing.ClassVar[Symbology]  # value = <Symbology.HIBC_AZTEC: 112>
    HIBC_BLOCKF: typing.ClassVar[Symbology]  # value = <Symbology.HIBC_BLOCKF: 110>
    HIBC_DM: typing.ClassVar[Symbology]  # value = <Symbology.HIBC_DM: 102>
    HIBC_MICPDF: typing.ClassVar[Symbology]  # value = <Symbology.HIBC_MICPDF: 108>
    HIBC_PDF: typing.ClassVar[Symbology]  # value = <Symbology.HIBC_PDF: 106>
    HIBC_QR: typing.ClassVar[Symbology]  # value = <Symbology.HIBC_QR: 104>
    ISBNX: typing.ClassVar[Symbology]  # value = <Symbology.ISBNX: 69>
    ITF14: typing.ClassVar[Symbology]  # value = <Symbology.ITF14: 89>
    JAPANPOST: typing.ClassVar[Symbology]  # value = <Symbology.JAPANPOST: 76>
    KIX: typing.ClassVar[Symbology]  # value = <Symbology.KIX: 90>
    KOREAPOST: typing.ClassVar[Symbology]  # value = <Symbology.KOREAPOST: 77>
    LOGMARS: typing.ClassVar[Symbology]  # value = <Symbology.LOGMARS: 50>
    MAILMARK_2D: typing.ClassVar[Symbology]  # value = <Symbology.MAILMARK_2D: 119>
    MAILMARK_4S: typing.ClassVar[Symbology]  # value = <Symbology.MAILMARK_4S: 121>
    MAXICODE: typing.ClassVar[Symbology]  # value = <Symbology.MAXICODE: 57>
    MICROPDF417: typing.ClassVar[Symbology]  # value = <Symbology.MICROPDF417: 84>
    MICROQR: typing.ClassVar[Symbology]  # value = <Symbology.MICROQR: 97>
    MSI_PLESSEY: typing.ClassVar[Symbology]  # value = <Symbology.MSI_PLESSEY: 47>
    NVE18: typing.ClassVar[Symbology]  # value = <Symbology.NVE18: 75>
    PDF417: typing.ClassVar[Symbology]  # value = <Symbology.PDF417: 55>
    PDF417COMP: typing.ClassVar[Symbology]  # value = <Symbology.PDF417COMP: 56>
    PHARMA: typing.ClassVar[Symbology]  # value = <Symbology.PHARMA: 51>
    PHARMA_TWO: typing.ClassVar[Symbology]  # value = <Symbology.PHARMA_TWO: 53>
    PLANET: typing.ClassVar[Symbology]  # value = <Symbology.PLANET: 82>
    PLESSEY: typing.ClassVar[Symbology]  # value = <Symbology.PLESSEY: 86>
    POSTNET: typing.ClassVar[Symbology]  # value = <Symbology.POSTNET: 40>
    PZN: typing.ClassVar[Symbology]  # value = <Symbology.PZN: 52>
    QRCODE: typing.ClassVar[Symbology]  # value = <Symbology.QRCODE: 58>
    RM4SCC: typing.ClassVar[Symbology]  # value = <Symbology.RM4SCC: 70>
    RMQR: typing.ClassVar[Symbology]  # value = <Symbology.RMQR: 145>
    TELEPEN: typing.ClassVar[Symbology]  # value = <Symbology.TELEPEN: 32>
    TELEPEN_NUM: typing.ClassVar[Symbology]  # value = <Symbology.TELEPEN_NUM: 87>
    ULTRA: typing.ClassVar[Symbology]  # value = <Symbology.ULTRA: 144>
    UPCA: typing.ClassVar[Symbology]  # value = <Symbology.UPCA: 34>
    UPCA_CC: typing.ClassVar[Symbology]  # value = <Symbology.UPCA_CC: 135>
    UPCA_CHK: typing.ClassVar[Symbology]  # value = <Symbology.UPCA_CHK: 35>
    UPCE: typing.ClassVar[Symbology]  # value = <Symbology.UPCE: 37>
    UPCE_CC: typing.ClassVar[Symbology]  # value = <Symbology.UPCE_CC: 136>
    UPCE_CHK: typing.ClassVar[Symbology]  # value = <Symbology.UPCE_CHK: 38>
    UPNQR: typing.ClassVar[Symbology]  # value = <Symbology.UPNQR: 143>
    UPU_S10: typing.ClassVar[Symbology]  # value = <Symbology.UPU_S10: 120>
    USPS_IMAIL: typing.ClassVar[Symbology]  # value = <Symbology.USPS_IMAIL: 85>
    VIN: typing.ClassVar[Symbology]  # value = <Symbology.VIN: 73>
    __members__: typing.ClassVar[dict[str, Symbology]]  # value = {'CODE11': <Symbology.CODE11: 1>, 'C25STANDARD': <Symbology.C25STANDARD: 2>, 'C25INTER': <Symbology.C25INTER: 3>, 'C25IATA': <Symbology.C25IATA: 4>, 'C25LOGIC': <Symbology.C25LOGIC: 6>, 'C25IND': <Symbology.C25IND: 7>, 'CODE39': <Symbology.CODE39: 8>, 'EXCODE39': <Symbology.EXCODE39: 9>, 'EANX': <Symbology.EANX: 13>, 'EANX_CHK': <Symbology.EANX_CHK: 14>, 'GS1_128': <Symbology.GS1_128: 16>, 'CODABAR': <Symbology.CODABAR: 18>, 'CODE128': <Symbology.CODE128: 20>, 'DPLEIT': <Symbology.DPLEIT: 21>, 'DPIDENT': <Symbology.DPIDENT: 22>, 'CODE16K': <Symbology.CODE16K: 23>, 'CODE49': <Symbology.CODE49: 24>, 'CODE93': <Symbology.CODE93: 25>, 'FLAT': <Symbology.FLAT: 28>, 'DBAR_OMN': <Symbology.DBAR_OMN: 29>, 'DBAR_LTD': <Symbology.DBAR_LTD: 30>, 'DBAR_EXP': <Symbology.DBAR_EXP: 31>, 'TELEPEN': <Symbology.TELEPEN: 32>, 'UPCA': <Symbology.UPCA: 34>, 'UPCA_CHK': <Symbology.UPCA_CHK: 35>, 'UPCE': <Symbology.UPCE: 37>, 'UPCE_CHK': <Symbology.UPCE_CHK: 38>, 'POSTNET': <Symbology.POSTNET: 40>, 'MSI_PLESSEY': <Symbology.MSI_PLESSEY: 47>, 'FIM': <Symbology.FIM: 49>, 'LOGMARS': <Symbology.LOGMARS: 50>, 'PHARMA': <Symbology.PHARMA: 51>, 'PZN': <Symbology.PZN: 52>, 'PHARMA_TWO': <Symbology.PHARMA_TWO: 53>, 'CEPNET': <Symbology.CEPNET: 54>, 'PDF417': <Symbology.PDF417: 55>, 'PDF417COMP': <Symbology.PDF417COMP: 56>, 'MAXICODE': <Symbology.MAXICODE: 57>, 'QRCODE': <Symbology.QRCODE: 58>, 'CODE128AB': <Symbology.CODE128AB: 60>, 'AUSPOST': <Symbology.AUSPOST: 63>, 'AUSREPLY': <Symbology.AUSREPLY: 66>, 'AUSROUTE': <Symbology.AUSROUTE: 67>, 'AUSREDIRECT': <Symbology.AUSREDIRECT: 68>, 'ISBNX': <Symbology.ISBNX: 69>, 'RM4SCC': <Symbology.RM4SCC: 70>, 'DATAMATRIX': <Symbology.DATAMATRIX: 71>, 'EAN14': <Symbology.EAN14: 72>, 'VIN': <Symbology.VIN: 73>, 'CODABLOCKF': <Symbology.CODABLOCKF: 74>, 'NVE18': <Symbology.NVE18: 75>, 'JAPANPOST': <Symbology.JAPANPOST: 76>, 'KOREAPOST': <Symbology.KOREAPOST: 77>, 'DBAR_STK': <Symbology.DBAR_STK: 79>, 'DBAR_OMNSTK': <Symbology.DBAR_OMNSTK: 80>, 'DBAR_EXPSTK': <Symbology.DBAR_EXPSTK: 81>, 'PLANET': <Symbology.PLANET: 82>, 'MICROPDF417': <Symbology.MICROPDF417: 84>, 'USPS_IMAIL': <Symbology.USPS_IMAIL: 85>, 'PLESSEY': <Symbology.PLESSEY: 86>, 'TELEPEN_NUM': <Symbology.TELEPEN_NUM: 87>, 'ITF14': <Symbology.ITF14: 89>, 'KIX': <Symbology.KIX: 90>, 'AZTEC': <Symbology.AZTEC: 92>, 'DAFT': <Symbology.DAFT: 93>, 'DPD': <Symbology.DPD: 96>, 'MICROQR': <Symbology.MICROQR: 97>, 'HIBC_128': <Symbology.HIBC_128: 98>, 'HIBC_39': <Symbology.HIBC_39: 99>, 'HIBC_DM': <Symbology.HIBC_DM: 102>, 'HIBC_QR': <Symbology.HIBC_QR: 104>, 'HIBC_PDF': <Symbology.HIBC_PDF: 106>, 'HIBC_MICPDF': <Symbology.HIBC_MICPDF: 108>, 'HIBC_BLOCKF': <Symbology.HIBC_BLOCKF: 110>, 'HIBC_AZTEC': <Symbology.HIBC_AZTEC: 112>, 'DOTCODE': <Symbology.DOTCODE: 115>, 'HANXIN': <Symbology.HANXIN: 116>, 'MAILMARK_2D': <Symbology.MAILMARK_2D: 119>, 'UPU_S10': <Symbology.UPU_S10: 120>, 'MAILMARK_4S': <Symbology.MAILMARK_4S: 121>, 'AZRUNE': <Symbology.AZRUNE: 128>, 'CODE32': <Symbology.CODE32: 129>, 'EANX_CC': <Symbology.EANX_CC: 130>, 'GS1_128_CC': <Symbology.GS1_128_CC: 131>, 'DBAR_OMN_CC': <Symbology.DBAR_OMN_CC: 132>, 'DBAR_LTD_CC': <Symbology.DBAR_LTD_CC: 133>, 'DBAR_EXP_CC': <Symbology.DBAR_EXP_CC: 134>, 'UPCA_CC': <Symbology.UPCA_CC: 135>, 'UPCE_CC': <Symbology.UPCE_CC: 136>, 'DBAR_STK_CC': <Symbology.DBAR_STK_CC: 137>, 'DBAR_OMNSTK_CC': <Symbology.DBAR_OMNSTK_CC: 138>, 'DBAR_EXPSTK_CC': <Symbology.DBAR_EXPSTK_CC: 139>, 'CHANNEL': <Symbology.CHANNEL: 140>, 'CODEONE': <Symbology.CODEONE: 141>, 'GRIDMATRIX': <Symbology.GRIDMATRIX: 142>, 'UPNQR': <Symbology.UPNQR: 143>, 'ULTRA': <Symbology.ULTRA: 144>, 'RMQR': <Symbology.RMQR: 145>, 'BC412': <Symbology.BC412: 146>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class UltracodeOptions:
    """
    Ultracode specific option (`symbol->option_3`)
    
    Members:
    
      ULTRA_COMPRESSION : Enable Ultracode compression (experimental)
    """
    ULTRA_COMPRESSION: typing.ClassVar[UltracodeOptions]  # value = <UltracodeOptions.ULTRA_COMPRESSION: 128>
    __members__: typing.ClassVar[dict[str, UltracodeOptions]]  # value = {'ULTRA_COMPRESSION': <UltracodeOptions.ULTRA_COMPRESSION: 128>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Vector:
    @property
    def circles(self) -> VectorCircles:
        """
        Iterable over circles
        """
    @property
    def height(self) -> float:
        """
        Height of barcode image (including text, whitespace)
        """
    @property
    def hexagons(self) -> VectorHexagons:
        """
        Iterable over hexagons
        """
    @property
    def rectangles(self) -> VectorRects:
        """
        Iterable over rectangles
        """
    @property
    def strings(self) -> VectorStrings:
        """
        Iterable over strings
        """
    @property
    def width(self) -> float:
        """
        Width of barcode image (including text, whitespace)
        """
class VectorCircle:
    @property
    def color(self) -> int:
        """
        Zero for draw with foreground colour (else draw with background colour (legacy)). Alias of `colour`
        """
    @property
    def colour(self) -> int:
        """
        Zero for draw with foreground colour (else draw with background colour (legacy))
        """
    @property
    def diameter(self) -> float:
        """
        Circle diameter. Does not include width (if any)
        """
    @property
    def next(self) -> VectorCircle:
        """
        Next circle
        """
    @property
    def width(self) -> float:
        """
        Width of circle perimeter (circumference). 0 for fill (disc)
        """
    @property
    def x(self) -> float:
        """
        Centre
        """
    @property
    def y(self) -> float:
        """
        Centre
        """
class VectorCircles:
    def __iter__(self) -> typing.Iterator[VectorCircle]:
        ...
    def __len__(self) -> int:
        ...
class VectorHexagon:
    @property
    def diameter(self) -> float:
        """
        Short (minimal) diameter (i.e. diameter of inscribed circle)
        """
    @property
    def next(self) -> VectorHexagon:
        """
        Next hexagon
        """
    @property
    def rotation(self) -> int:
        """
        0, 90, 180, 270 degrees, where 0 has apex at top, i.e. short diameter is horizontal
        """
    @property
    def x(self) -> float:
        """
        Centre
        """
    @property
    def y(self) -> float:
        """
        Centre
        """
class VectorHexagons:
    def __iter__(self) -> typing.Iterator[VectorHexagon]:
        ...
    def __len__(self) -> int:
        ...
class VectorRect:
    @property
    def color(self) -> int:
        """
        -1 for foreground, 1-8 for Cyan, Blue, Magenta, Red, Yellow, Green, Black, White. Alias of `colour`
        """
    @property
    def colour(self) -> int:
        """
        -1 for foreground, 1-8 for Cyan, Blue, Magenta, Red, Yellow, Green, Black, White
        """
    @property
    def height(self) -> float:
        ...
    @property
    def next(self) -> VectorRect:
        """
        Next rectangle
        """
    @property
    def width(self) -> float:
        ...
    @property
    def x(self) -> float:
        """
        Left
        """
    @property
    def y(self) -> float:
        """
        Top
        """
class VectorRects:
    def __iter__(self) -> typing.Iterator[VectorRect]:
        ...
    def __len__(self) -> int:
        ...
class VectorString:
    @property
    def fsize(self) -> float:
        """
        Font size
        """
    @property
    def halign(self) -> int:
        """
        Horizontal alignment: 0 for centre, 1 for left, 2 for right (end)
        """
    @property
    def length(self) -> int:
        """
        Number of characters (bytes)
        """
    @property
    def next(self) -> VectorString:
        """
        Next string
        """
    @property
    def rotation(self) -> int:
        """
        0, 90, 180, 270 degrees
        """
    @property
    def text(self) -> str:
        ...
    @property
    def width(self) -> float:
        """
        Rendered width estimate
        """
    @property
    def x(self) -> float:
        """
        Relative to halign (i.e. centre, left, right)
        """
    @property
    def y(self) -> float:
        """
        Relative to baseline
        """
class VectorStrings:
    def __iter__(self) -> typing.Iterator[VectorString]:
        ...
    def __len__(self) -> int:
        ...
class WarningLevel:
    """
    Warning level (`symbol->warn_level`)
    
    Members:
    
      DEFAULT : Default behaviour
    
      FAIL_ALL : Treat warning as error
    """
    DEFAULT: typing.ClassVar[WarningLevel]  # value = <WarningLevel.DEFAULT: 0>
    FAIL_ALL: typing.ClassVar[WarningLevel]  # value = <WarningLevel.FAIL_ALL: 2>
    __members__: typing.ClassVar[dict[str, WarningLevel]]  # value = {'DEFAULT': <WarningLevel.DEFAULT: 0>, 'FAIL_ALL': <WarningLevel.FAIL_ALL: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
__version__: str = '0.1.0'
__zint_version__: str = '2.13.0'
