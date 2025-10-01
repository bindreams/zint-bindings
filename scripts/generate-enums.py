"""Generate src/generated/enums.hpp file. Run this from the root directory."""

import io
import json
import re
import sys
from dataclasses import dataclass
from textwrap import dedent

re_base_define = r"^#define (\w+) +((?:0x)?\d+)"
"""`#define BARCODE_CODE128 0x01`"""

re_comment = r"\/\* ([^\n]*) \*\/"
"""`/* This is barcode documentation */`"""

re_comment_note = r"\n *\/\* (.*?)\s+?\*\/"
"""`/* Barcode note, starting from next line */`"""

re_define = re_base_define + " *" + re_comment + "(?:" + re_comment_note + ")?"


@dataclass
class EnumInfo:
    name: str
    values: list
    cpp_base: str = "int"
    py_base: str = "enum.Enum"
    docstring: str = ""


def find_line_re(pattern, source: str, start=0):
    m = re.search(pattern, source[start:], re.MULTILINE | re.DOTALL)
    if m:
        return m.start() + start

    return None


def escape_string(s: str):
    """Escape a string for double quotes in C++."""
    return json.dumps(s, ensure_ascii=False)[1:-1]


def parse_enum_values(
    source: str,
    *,
    header: str,
    footer: str = r"^\/\*",
    prefix=None,
    suffix=None,
    blacklist=None,
):
    enum_values = {}
    enum_comments = {}

    start = find_line_re(header, source)
    start = source.find("\n", start) + 1
    end = find_line_re(footer, source, start)
    text = source[start:end]

    for m in re.finditer(re_define, text, re.MULTILINE | re.DOTALL):
        # Macro name
        name = m[1]
        if prefix is not None:
            assert name.startswith(prefix)
            name = name[len(prefix) :]

        if suffix is not None:
            assert name.endswith(suffix)
            name = name[: -len(suffix)]

        # Macro value
        value = m[2]
        if value.startswith("0x"):
            value = int(value, 16)
        else:
            value = int(value)

        # Comment
        comment = m[3]
        if m[4] is not None:  # Note after the comment
            comment = comment + ". " + m[4]

        if blacklist is not None and blacklist(name, value, comment):
            continue

        enum_values[name] = value
        enum_comments[name] = comment

    enum = [(name, enum_values[name], enum_comments[name]) for name in enum_values]
    enum.sort(key=lambda item: item[1])
    return enum


def enum_definition(enum, *, class_name: str, base_type: str = "int"):
    values = ",".join(f"{name} = {value}" for name, value, _ in enum)
    return f"enum class {class_name} : {base_type} {{ {values} }};"


def write_enum_macro(fd, enum: EnumInfo):
    fd.write(f'ENUM_BEGIN({enum.name}, {enum.cpp_base}, "{enum.py_base}", "{escape_string(enum.docstring)}")\n')

    for name, value, value_docstring in enum.values:
        fd.write(f'ENUM_VALUE({enum.name}, {name}, {value}, "{escape_string(value_docstring)}")\n')

    fd.write(f"ENUM_END({enum.name})\n\n")


def main():
    with open("external/zint/backend/zint.h", "r", encoding="utf-8") as f:
        source = f.read()

    enums = [
        EnumInfo(
            name="Symbology",
            docstring="Values for `Symbol.symbology`",
            values=parse_enum_values(
                source,
                header=re.escape("/* Symbologies (`symbol->symbology`) */"),
                prefix="BARCODE_",
                blacklist=lambda name, _, comment: comment == "Legacy" or name == "LAST",
            ),
        ),
        EnumInfo(
            name="OutputOptions",
            docstring="Values for `Symbol.output_options`",
            py_base="enum.Flag",
            values=parse_enum_values(
                source,
                header=re.escape("/* Output options (`symbol->output_options`) */"),
            ),
        ),
        EnumInfo(
            name="InputMode",
            docstring="Values for `Symbol.input_mode`",
            py_base="enum.Flag",
            values=parse_enum_values(
                source,
                header=re.escape("/* Input data types (`symbol->input_mode`) */"),
                footer=r"^\/\*(?! The following may be OR-ed with above)",  # Do not terminate on a top-level comment
                suffix="_MODE",
            ),
        ),
        EnumInfo(
            name="DataMatrixOptions",
            docstring="Data Matrix specific options (`symbol->option_3`)",
            py_base="enum.IntEnum",
            values=parse_enum_values(
                source,
                header=re.escape("/* Data Matrix specific options (`symbol->option_3`) */"),
                prefix="DM_",
            ),
        ),
        EnumInfo(
            name="QrFamilyOptions",
            docstring="QR, Han Xin, Grid Matrix specific options (`symbol->option_3`)",
            py_base="enum.IntEnum",
            values=parse_enum_values(
                source,
                header=re.escape("/* QR, Han Xin, Grid Matrix specific options (`symbol->option_3`) */"),
                prefix="ZINT_",
            ),
        ),
        EnumInfo(
            name="UltracodeOptions",
            docstring="Ultracode specific option (`symbol->option_3`)",
            py_base="enum.IntEnum",
            values=parse_enum_values(
                source,
                header=re.escape("/* Ultracode specific option (`symbol->option_3`) */"),
            ),
        ),
        EnumInfo(
            name="WarningLevel",
            docstring="Warning level (`symbol->warn_level`)",
            values=parse_enum_values(
                source,
                header=re.escape("/* Warning level (`symbol->warn_level`) */"),
                prefix="WARN_",
            ),
        ),
        EnumInfo(
            name="CapabilityFlags",
            docstring="Capability flags (ZBarcode_Cap() `cap_flag`)",
            cpp_base="unsigned int",
            py_base="enum.Flag",
            values=parse_enum_values(
                source,
                header=re.escape("/* Capability flags (ZBarcode_Cap() `cap_flag`) */"),
                prefix="ZINT_CAP_",
                blacklist=lambda _1, _2, comment: comment == "Legacy",
            ),
        ),
    ]

    # Write files ------------------------------------------------------------------------------------------------------
    # Write enums.inc
    with open("src/generated/enums.inc", "w", encoding="utf-8", newline="\n") as fd:
        for enum in enums:
            write_enum_macro(fd, enum)


if __name__ == "__main__":
    sys.exit(main())
