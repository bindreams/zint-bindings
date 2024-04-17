"""This script impersonates 'pybind11-stubgen' script.

pybind11-stubgen does not have a usable API, so instead this script pre-imports zint from a pyd/so file, and then
expects to be called for generating zint type annotations.
"""

import sys

import pybind11_stubgen

# Pre-import zint from a pyd/so file. pybind11_stubgen fails on non-installed modules otherwise.
sys.path.insert(0, ".")
import zint

pybind11_stubgen.main()
