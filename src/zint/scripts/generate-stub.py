"""Generate a stub file from a compiled module.

This script is supposed to be run from the "build" directory after the zint module has been compiled. It generates
a stub file using "pybind11-stubgen", then formats it using the "black" formatter.

pybind11-stubgen does not have a usable API, so instead this script pre-imports zint from a pyd/so file, and then
substitutes argv with arguments for pybind11-stubgen.
"""

import argparse
import importlib._bootstrap_external
import importlib.util
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable, Union

import pybind11_stubgen
import yapf.yapflib.yapf_api as yapf
from yapf.yapflib.file_resources import \
    GetDefaultStyleForDir as find_yapf_style

PYC_MAGIC = importlib.util.MAGIC_NUMBER
EXT_MAGIC = {
    # win32 DLL
    b"MZ",
    # ELF
    b"\x7FELF",
    # Mach-O
    b"\xFE\xED\xFA\xCE",
    b"\xCE\xFA\xED\xFE",
    b"\xFE\xED\xFA\xCF",
    b"\xCF\xFA\xED\xFE",
    b"\xCA\xFE\xBA\xBE",
}


def file_startswith(path, magic: bytes):
    with open(path, "rb") as fp:
        contents = fp.read(len(magic))
    return contents == magic


def truestem(path):
    path = Path(path)
    suffixes = "".join(path.suffixes)
    return path.name[:-len(suffixes)]


def module(path, name=None):
    path = str(Path(path).resolve())

    if name is None:
        name = truestem(path)

    if file_startswith(path, PYC_MAGIC):
        loader = importlib._bootstrap_external.SourcelessFileLoader(name, path)
    elif any(file_startswith(path, magic) for magic in EXT_MAGIC):
        loader = importlib._bootstrap_external.ExtensionFileLoader(name, path)
    else:
        loader = importlib._bootstrap_external.SourceFileLoader(name, path)

    spec = importlib.util.spec_from_loader(name, loader)
    assert spec is not None
    assert spec.loader is not None
    assert spec.loader is loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def importfile(path):
    m = module(path)
    sys.modules[m.__name__] = m
    return m


@contextmanager
def argv(new: Iterable):
    new = [str(item) for item in new]
    old, sys.argv = sys.argv, new
    try:
        yield None
    finally:
        sys.argv = old


@contextmanager
def chdir(path):
    """Polyfill for contextlib.chdir. Remove oldest supported python is >= 3.11"""
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def stub(path):
    name = importfile(path).__name__
    with TemporaryDirectory() as tempdir, argv([sys.argv[0], "--output-dir", tempdir, "--exit-code", name]):
        pybind11_stubgen.main()
        with open(f"{tempdir}/{name}.pyi", "r", encoding="utf-8") as fp:
            return fp.read()


def format(text: str, config_path: Union[Path, str]):
    config_path = Path(config_path)
    if config_path.is_dir():
        config_path = find_yapf_style(config_path)

    result, _ = yapf.FormatCode(text, style_config=str(config_path))
    return result


def cli():
    parser = argparse.ArgumentParser("generate-stub")
    parser.add_argument("module", type=Path, help="path to source module")
    parser.add_argument("-o", "--output", type=Path, default=None, help="write to file instead of stdout")
    parser.add_argument(
        "--format-config", default=None, help="path to format config file or a directory under a config scope"
    )

    return parser


def main():
    args = cli().parse_args()
    text = stub(args.module)
    if args.format_config is not None:
        text = format(text, args.format_config)

    if args.output is not None:
        with open(args.output, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    sys.exit(main())
