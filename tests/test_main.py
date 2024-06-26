import logging

from zint import InputMode, Seg, Symbol, Symbology, CapabilityFlags, DataMatrixOptions, QrFamilyOptions, UltracodeOptions, OutputOptions, WarningLevel


def test_basic_usage():
    s = Symbol()
    s.symbology = Symbology.DATAMATRIX
    s.encode(b"Hi mom!")
    s.buffer(0)

    assert s.bitmap is not None
    assert s.bitmap.shape == (28, 28, 3)


def test_warnings(caplog):
    s = Symbol()
    s.symbology = Symbology.AZTEC
    s.option_1 = 10  # Incorrect option
    s.encode(b"Hello")

    logs = caplog.records
    assert len(logs) == 1
    assert logs[0].name == "zint"
    assert logs[0].levelno == logging.WARNING
    assert logs[0].msg == "Warning 503: Invalid error correction level - using default instead"


def test_segments():
    s = Symbol()
    s.symbology = Symbology.DATAMATRIX

    # Test that any iterable will be accepted
    seg1 = Seg()
    seg1.source = b"abc"
    seg1.eci = 899

    seg2 = Seg()
    seg2.source = b"def"
    seg2.eci = 3

    def gen():
        yield seg1
        yield seg2

    s.encode_segs(gen())


def test_vector():
    s = Symbol()
    s.symbology = Symbology.MAXICODE
    s.primary = "152382802000000"
    s.encode(rb"1Z00004951\GUPSN\G06X610\G159\G1234567\G1/1\G\GY\G1 MAIN ST\GNY\GNY\R\E")
    s.buffer_vector()

    size = 0
    for _ in s.vector.hexagons:
        size += 1
    assert size == len(s.vector.hexagons)

    size = 0
    for _ in s.vector.circles:
        size += 1
    assert size == len(s.vector.circles)


def test_enum_input_output_mode():
    """Test that the input_mode is assignable from an enum."""
    s = Symbol()
    s.input_mode |= InputMode.UNICODE | InputMode.FAST
    s.output_options |= OutputOptions.BARCODE_BIND | OutputOptions.BARCODE_NO_QUIET_ZONES


def test_enum_warn_level():
    s = Symbol()
    s.warn_level = WarningLevel.FAIL_ALL


def test_enum_docstrings():
    # Test that docstring for enums have been added to the module
    assert Symbology.__doc__ == "Values for `Symbol.symbology`"
    assert Symbology.DATAMATRIX.__doc__ == "Data Matrix (ECC200)"

def test_enum_options():
    s = Symbol()
    s.symbology = Symbology.DATAMATRIX
    s.option_3 = DataMatrixOptions.ISO_144

    s.symbology = Symbology.QRCODE
    s.option_3 = QrFamilyOptions.FULL_MULTIBYTE

    s.symbology = Symbology.ULTRA
    s.option_3 = UltracodeOptions.ULTRA_COMPRESSION

def test_capabilities():
    assert Symbol.capabilities(Symbology.DATAMATRIX) & CapabilityFlags.GS1
    assert not (Symbol.capabilities(Symbology.DATAMATRIX) & CapabilityFlags.HRT)

    assert not (Symbol.capabilities(Symbology.CODE128) & CapabilityFlags.GS1)
    assert Symbol.capabilities(Symbology.CODE128) & CapabilityFlags.HRT
