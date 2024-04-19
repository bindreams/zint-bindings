"""Generate a stub file from a compiled module.

This script is supposed to be run from the "build" directory after the zint module has been compiled. It generates
a stub file using "pybind11-stubgen", then formats it using the "black" formatter.

pybind11-stubgen does not have a usable API, so instead this script pre-imports zint from a pyd/so file, and then
substitutes argv with arguments for pybind11-stubgen.
"""

import sys
from pathlib import Path

import black
import pybind11_stubgen


def main():
    # Create pyi stub --------------------------------------------------------------------------------------------------
    argv_ = sys.argv
    try:
        sys.argv = [
            "scripts/generate-stub.py",
            "--output-dir",
            "zint-stubs",
            "--numpy-array-use-type-var",
            "--exit-code",
            "zint",
        ]
        # Pre-import zint from a pyd/so file. pybind11_stubgen fails on non-installed modules otherwise.
        sys.path.insert(0, ".")
        import zint

        pybind11_stubgen.main()
    finally:
        sys.argv = argv_

    # Rename stub to a correct name and format it ----------------------------------------------------------------------
    stub = Path("zint-stubs/zint.pyi")
    assert stub.exists()
    stub = stub.replace("zint-stubs/__init__.pyi")

    black.main([str(stub), "--quiet"], standalone_mode=False)


if __name__ == "__main__":
    sys.exit(main())
