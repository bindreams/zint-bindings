import logging

from zint import Seg, Symbol, Symbology


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
