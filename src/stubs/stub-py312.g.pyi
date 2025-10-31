"""
A barcode encoding library supporting over 50 symbologies.
"""
from __future__ import annotations
import collections.abc
import enum
import typing

__all__: list = [
    'Symbol', 'Symbology', 'Seg', 'StructApp', 'Vector', 'VectorCircle', 'VectorHexagon', 'VectorRect', 'VectorString',
    'CapabilityFlags', 'DataMatrixOptions', 'InputMode', 'OutputOptions', 'QrFamilyOptions', 'UltracodeOptions',
    'WarningLevel'
]


class CapabilityFlags(enum.Flag):
    """
    Capability flags (ZBarcode_Cap() `cap_flag`)
    """
    COMPLIANT_HEIGHT: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.COMPLIANT_HEIGHT: 8192>
    COMPOSITE: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.COMPOSITE: 8>
    DOTTY: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.DOTTY: 64>
    EANUPC: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.EANUPC: 4>
    ECI: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.ECI: 16>
    FIXED_RATIO: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.FIXED_RATIO: 256>
    FULL_MULTIBYTE: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.FULL_MULTIBYTE: 1024>
    GS1: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.GS1: 32>
    HRT: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.HRT: 1>
    MASK: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.MASK: 2048>
    QUIET_ZONES: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.QUIET_ZONES: 128>
    READER_INIT: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.READER_INIT: 512>
    STACKABLE: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.STACKABLE: 2>
    STRUCTAPP: typing.ClassVar[CapabilityFlags]  # value = <CapabilityFlags.STRUCTAPP: 4096>


class DataMatrixOptions(enum.IntEnum):
    """
    Data Matrix specific options (`symbol->option_3`)
    """
    DMRE: typing.ClassVar[DataMatrixOptions]  # value = <DataMatrixOptions.DMRE: 101>
    ISO_144: typing.ClassVar[DataMatrixOptions]  # value = <DataMatrixOptions.ISO_144: 128>
    SQUARE: typing.ClassVar[DataMatrixOptions]  # value = <DataMatrixOptions.SQUARE: 100>

    @classmethod
    def __new__(cls, value):
        ...

    def __format__(self, format_spec):
        """
        Convert to a string according to format_spec.
        """


class InputMode(enum.Flag):
    """
    Values for `Symbol.input_mode`
    """
    ESCAPE: typing.ClassVar[InputMode]  # value = <InputMode.ESCAPE: 8>
    EXTRA_ESCAPE: typing.ClassVar[InputMode]  # value = <InputMode.EXTRA_ESCAPE: 256>
    FAST: typing.ClassVar[InputMode]  # value = <InputMode.FAST: 128>
    GS1: typing.ClassVar[InputMode]  # value = <InputMode.GS1: 2>
    GS1NOCHECK: typing.ClassVar[InputMode]  # value = <InputMode.GS1NOCHECK: 32>
    GS1PARENS: typing.ClassVar[InputMode]  # value = <InputMode.GS1PARENS: 16>
    HEIGHTPERROW: typing.ClassVar[InputMode]  # value = <InputMode.HEIGHTPERROW: 64>
    UNICODE: typing.ClassVar[InputMode]  # value = <InputMode.UNICODE: 1>


class OutputOptions(enum.Flag):
    """
    Values for `Symbol.output_options`
    """
    BARCODE_BIND: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_BIND: 2>
    BARCODE_BIND_TOP: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_BIND_TOP: 1>
    BARCODE_BOX: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_BOX: 4>
    BARCODE_DOTTY_MODE: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_DOTTY_MODE: 256>
    BARCODE_MEMORY_FILE: typing.ClassVar[OutputOptions]  # value = <OutputOptions.BARCODE_MEMORY_FILE: 65536>
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


class QrFamilyOptions(enum.IntEnum):
    """
    QR, Han Xin, Grid Matrix specific options (`symbol->option_3`)
    """
    FULL_MULTIBYTE: typing.ClassVar[QrFamilyOptions]  # value = <QrFamilyOptions.FULL_MULTIBYTE: 200>

    @classmethod
    def __new__(cls, value):
        ...

    def __format__(self, format_spec):
        """
        Convert to a string according to format_spec.
        """


class Seg:
    """
    Segment for use with `Symbol.encode_segs`.
    """

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, arg0: collections.abc.Buffer, arg1: typing.SupportsInt) -> None:
        ...

    @property
    def eci(self) -> int:
        """
        Extended Channel Interpretation
        """

    @eci.setter
    def eci(self, arg0: typing.SupportsInt) -> None:
        ...

    @property
    def source(self) -> memoryview:
        """
        Data to encode
        """

    @source.setter
    def source(self, arg1: collections.abc.Buffer) -> None:
        ...


class StructApp:
    """
    Structural append information (see `Symbol.structapp`).
    
    Ignored unless `StructApp.count` is non-zero
    """

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, index: typing.SupportsInt, count: typing.SupportsInt, id: bytes = b'') -> None:
        ...

    @property
    def count(self) -> int:
        """
        Number of symbols in Structured Append sequence. Set >= 2 to add SA Info
        """

    @count.setter
    def count(self, arg0: typing.SupportsInt) -> None:
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
    def index(self, arg0: typing.SupportsInt) -> None:
        ...


class Symbol:
    """
    Main symbol structure.
    """

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
    def scale_from_xdim_dp(
        symbology: Symbology,
        /,
        x_dim_mm: typing.SupportsFloat,
        *,
        dpmm: typing.SupportsFloat,
        filetype: str | None = None
    ) -> float:
        """
        Return the scale to use for `symbology` for non-zero X-dimension `x_dim_mm` at `dpmm` dots per mm for `filetype`. If `dpmm` zero defaults to 12. If `filetype` is None, defaults to "GIF". Returns 0 on error
        """

    @staticmethod
    def xdim_dp_from_scale(
        symbology: Symbology,
        /,
        scale: typing.SupportsFloat,
        *,
        x_dim_mm_or_dpmm: typing.SupportsFloat,
        filetype: str | None = None
    ) -> float:
        """
        Reverse of `Symbol.scale_from_xdim_dp`. Estimate the X-dimension or dpmm given non-zero `scale` and non-zero `x_dim_mm_or_dpmm`. Return value bound to dpmm max not X-dimension max. Returns 0 on error
        """

    def __init__(self) -> None:
        ...

    def buffer(self, rotate_deg: typing.SupportsInt = 0) -> None:
        """
        Output a previously encoded symbol to memory as raster (`Symbol.bitmap`)
        """

    def buffer_vector(self, rotate_deg: typing.SupportsInt = 0) -> None:
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
    def encode_segs(self, segs: collections.abc.Sequence[Seg]) -> None:
        """
        Encode a barcode with multiple ECI segments
        """

    @typing.overload
    def encode_segs(self, segs: collections.abc.Iterable) -> None:
        """
        Encode a barcode with multiple ECI segments
        """

    def print(self, rotate_deg: typing.SupportsInt = 0) -> None:
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
    def border_width(self, arg1: typing.SupportsInt) -> None:
        ...

    @property
    def debug(self) -> int:
        """
        Debugging flags
        """

    @debug.setter
    def debug(self, arg1: typing.SupportsInt) -> None:
        ...

    @property
    def dot_size(self) -> float:
        """
        Size of dots used in BARCODE_DOTTY_MODE. Default 0.8
        """

    @dot_size.setter
    def dot_size(self, arg1: typing.SupportsFloat) -> None:
        ...

    @property
    def dpmm(self) -> float:
        """
        Resolution of output in dots per mm (BMP/EMF/PCX/PNG/TIF only). Default 0 (none)
        """

    @dpmm.setter
    def dpmm(self, arg1: typing.SupportsFloat) -> None:
        ...

    @property
    def eci(self) -> int:
        """
        Extended Channel Interpretation. Default 0 (none)
        """

    @eci.setter
    def eci(self, arg1: typing.SupportsInt) -> None:
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
    def guard_descent(self, arg1: typing.SupportsFloat) -> None:
        ...

    @property
    def height(self) -> float:
        """
        Barcode height in X-dimensions (ignored for fixed-width barcodes)
        """

    @height.setter
    def height(self, arg1: typing.SupportsFloat) -> None:
        ...

    @property
    def input_mode(self) -> InputMode:
        """
        Encoding of input data (see `InputMode`). Default `InputMode.DATA`
        """

    @input_mode.setter
    def input_mode(self, arg1: InputMode) -> None:
        ...

    @property
    def memfile(self) -> memoryview | None:
        """
        In-memory file buffer if BARCODE_MEMORY_FILE (output only)
        """

    @property
    def option_1(self) -> int:
        """
        Symbol-specific options
        """

    @option_1.setter
    def option_1(self, arg1: typing.SupportsInt) -> None:
        ...

    @property
    def option_2(self) -> int:
        """
        Symbol-specific options
        """

    @option_2.setter
    def option_2(self, arg1: typing.SupportsInt) -> None:
        ...

    @property
    def option_3(self) -> int:
        """
        Symbol-specific options
        """

    @option_3.setter
    def option_3(self, arg1: typing.SupportsInt) -> None:
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
    def output_options(self) -> OutputOptions:
        """
        Various output parameters (bind, box etc, see `OutputOptions`)
        """

    @output_options.setter
    def output_options(self, arg1: OutputOptions) -> None:
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
    def row_height(self) -> list:
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
    def scale(self, arg1: typing.SupportsFloat) -> None:
        ...

    @property
    def show_hrt(self) -> bool:
        """
        If `True`, display Human Readable Text (HRT) on supported barcodes. Default `True`. Alias of `Symbol.show_text`.
        """

    @show_hrt.setter
    def show_hrt(self, arg1: bool) -> None:
        ...

    @property
    def show_text(self) -> bool:
        """
        If `True`, display Human Readable Text (HRT) on supported barcodes. Default `True`
        """

    @show_text.setter
    def show_text(self, arg1: bool) -> None:
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
        Symbol type to use (see `Symbology`)
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
        Gap between barcode and Human Readable Text (HRT) in X-dimensions. Default 1
        """

    @text_gap.setter
    def text_gap(self, arg1: typing.SupportsFloat) -> None:
        ...

    @property
    def vector(self) -> Vector:
        """
        Vector header (vector output only)
        """

    @property
    def warn_level(self) -> WarningLevel:
        """
        Affects error/warning value returned by Zint API (see `WarningLevel`)
        """

    @warn_level.setter
    def warn_level(self, arg1: WarningLevel) -> None:
        ...

    @property
    def whitespace_height(self) -> int:
        """
        Height in X-dimensions of whitespace above & below the barcode
        """

    @whitespace_height.setter
    def whitespace_height(self, arg1: typing.SupportsInt) -> None:
        ...

    @property
    def whitespace_width(self) -> int:
        """
        Width in X-dimensions of whitespace to left & right of barcode
        """

    @whitespace_width.setter
    def whitespace_width(self, arg1: typing.SupportsInt) -> None:
        ...

    @property
    def width(self) -> int:
        """
        Width of the generated symbol (output only)
        """


class Symbology(enum.Enum):
    """
    Values for `Symbol.symbology`
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
    DXFILMEDGE: typing.ClassVar[Symbology]  # value = <Symbology.DXFILMEDGE: 147>
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


class UltracodeOptions(enum.IntEnum):
    """
    Ultracode specific option (`symbol->option_3`)
    """
    ULTRA_COMPRESSION: typing.ClassVar[UltracodeOptions]  # value = <UltracodeOptions.ULTRA_COMPRESSION: 128>

    @classmethod
    def __new__(cls, value):
        ...

    def __format__(self, format_spec):
        """
        Convert to a string according to format_spec.
        """


class Vector:
    """
    Vector image information, returned from `Symbol.vector` after calling `Symbol.buffer_vector`
    """

    @property
    def circles(self) -> VectorCircles:
        """
        An iterable over circles (`VectorCircle`)
        """

    @property
    def height(self) -> float:
        """
        Height of barcode image (including text, whitespace)
        """

    @property
    def hexagons(self) -> VectorHexagons:
        """
        An iterable over hexagons (`VectorHexagon`)
        """

    @property
    def rectangles(self) -> VectorRects:
        """
        An iterable over rectangles (`VectorRectangle`)
        """

    @property
    def strings(self) -> VectorStrings:
        """
        An iterable over strings (`VectorString`)
        """

    @property
    def width(self) -> float:
        """
        Width of barcode image (including text, whitespace)
        """


class VectorCircle:
    """
    Circle vector elements returned from `Vector.circles`
    """

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

    def __iter__(self) -> collections.abc.Iterator[VectorCircle]:
        ...

    def __len__(self) -> int:
        ...


class VectorHexagon:
    """
    Hexagon vector elements returned from `Vector.hexagons`
    """

    @property
    def diameter(self) -> float:
        """
        Short (minimal) diameter (i.e. diameter of inscribed circle)
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

    def __iter__(self) -> collections.abc.Iterator[VectorHexagon]:
        ...

    def __len__(self) -> int:
        ...


class VectorRect:
    """
    Rectangle vector elements returned from `Vector.rectangles`
    """

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

    def __iter__(self) -> collections.abc.Iterator[VectorRect]:
        ...

    def __len__(self) -> int:
        ...


class VectorString:
    """
    String vector elements returned from `Vector.strings`
    """

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

    def __iter__(self) -> collections.abc.Iterator[VectorString]:
        ...

    def __len__(self) -> int:
        ...


class WarningLevel(enum.Enum):
    """
    Warning level (`symbol->warn_level`)
    """
    DEFAULT: typing.ClassVar[WarningLevel]  # value = <WarningLevel.DEFAULT: 0>
    FAIL_ALL: typing.ClassVar[WarningLevel]  # value = <WarningLevel.FAIL_ALL: 2>


__upstream_version__: str = '2.15.0'
__version__: str = '1.2.2'
