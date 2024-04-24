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
    r"zint\.__all__ is not present at runtime",
    # Filtered out because __all__ is a special variable and does not need to be present in the file.
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
