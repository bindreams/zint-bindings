"""Test generated stub file.

This script uses mypy's "stubtest" script to test the file. Some errors that mypy finds are allowed and this script
filters them out.
"""

import platform
import re
import subprocess as sp

import pytest

allowed_errors = [
    r"zint\.\w+ is inconsistent, metaclass differs",
    # Filtered out because the mentioned metaclass is a pybind11 implementation detail.
    r"zint\.\w+\.__init__ is inconsistent, stub does not have \*args argument \"args\"",
    # Filtered out because this error is raised for class which are not constructible from Python and don't have an
    # __init__ in the stub file.
    r"zint\.InputMode\.DATA is not present in stub",
    # Filtered out because of a bug in pybind11-stubgen, tracked in
    # https://github.com/sizmailov/pybind11-stubgen/issues/223
    r"zint\.\w+\.__new__ is inconsistent, stub argument \"value\" differs from runtime argument \"cls\"",
    r"zint\.\w+\.__new__ is inconsistent, stub does not have argument \"value\"",
    # I don't understand this error, I suspect stubtest is wrong and does not recognize classmethods.
    r"zint\.\w+\._pybind11_conduit_v1_ is inconsistent, stub is a staticmethod but runtime is not",
    # _pybind11_conduit_v1_ is an implementation detail of pybind11 and should have never appeared in the stub.
]

for i, pattern in enumerate(allowed_errors):
    allowed_errors[i] = re.compile(pattern)


@pytest.mark.skipif(
    platform.python_implementation() != "CPython", reason="stubtest does not work on non-CPython implementations"
)
def test_stub():
    sp.run(["stubtest", "--help"], check=True, stdout=sp.DEVNULL)  # Check that the executable works
    errors = sp.run(["stubtest", "zint"], check=False, text=True, stderr=sp.STDOUT, stdout=sp.PIPE).stdout

    fail = False
    sections = errors.split("\n\n")
    # Each section has the following format:
    # ```
    # error: zint.VectorRect.__init__ is inconsistent, stub does not have *args argument "args"
    # Stub: in file [...]
    # def (self: builtins.object)
    # Runtime:
    # def (self, /, *args, **kwargs)
    # ```

    for section in sections[:-1]:  # Last section of output is the summary
        assert section.startswith("error: ")
        error_text = section[len("error: ") :].split("\n")[0]
        ok = False

        for error in allowed_errors:
            if re.fullmatch(error, error_text):
                ok = True
                break

        if not ok:
            fail = True
            print(section, end="\n\n")

    if fail:
        pytest.fail("stubtest found errors which were not filtered (see output)")
